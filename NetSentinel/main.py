import sys
import asyncio
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from core.scanner import run_async_scan, COMMON_PORTS
from core.banner_grabber import enrich_service_banner
from core.cve_engine import analyze_vulnerabilities
from reports.generator import save_report

console = Console()

def display_banner():
    banner_text = "[bold cyan]🛡️ NetSentinel Vulnerability Engine v1.0.0[/bold cyan]\n[dim]Asynchronous Network Reconnaissance & Vulnerability Correlation[/dim]"
    console.print(Panel(banner_text, expand=False))

def parse_ports(port_arg: str) -> list[int]:
    """
    Parses flexible port arguments into a list of integers.
    Supports: '80,445', '1-100', or default lists.
    """
    if not port_arg:
        return COMMON_PORTS

    ports = set()
    for part in port_arg.split(","):
        part = part.strip()
        if "-" in part:
            try:
                start, end = part.split("-")
                ports.update(range(int(start), int(end) + 1))
            except ValueError:
                continue
        elif part.isdigit():
            ports.add(int(part))

    # Filter valid TCP port range (1-65535) and return sorted list
    valid_ports = sorted([p for p in ports if 1 <= p <= 65535])
    return valid_ports if valid_ports else COMMON_PORTS

def build_port_table(open_ports_with_services):
    table = Table(title="Open Ports & Identified Services", header_style="bold magenta")
    table.add_column("Port", style="cyan", justify="right")
    table.add_column("Service", style="green")
    table.add_column("Banner / Details", style="white")

    for item in open_ports_with_services:
        table.add_row(str(item["port"]), item["service"], item["banner_details"])
    return table

def build_vuln_table(vulnerabilities):
    table = Table(title="Vulnerability Correlation Findings", header_style="bold red")
    table.add_column("Severity", justify="center")
    table.add_column("CVE / Ref ID", style="yellow")
    table.add_column("Title", style="white")
    table.add_column("Port", justify="right", style="cyan")

    for v in vulnerabilities:
        sev = v["severity"]
        sev_style = "bold red" if sev in ["CRITICAL", "HIGH"] else "yellow" if sev == "MEDIUM" else "blue"
        table.add_row(f"[{sev_style}]{sev}[/{sev_style}]", v["cve_id"], v["title"], str(v["matched_port"]))
    return table

async def main():
    parser = argparse.ArgumentParser(description="NetSentinel - Network Vulnerability Scanner")
    parser.add_argument("--target", "-t", default="127.0.0.1", help="Target IP address or hostname (default: 127.0.0.1)")
    parser.add_argument("--ports", "-p", default=None, help="Ports to scan (e.g., '80,445', '1-1000', or '21,22,80-90')")
    args = parser.parse_args()

    display_banner()
    target = args.target
    target_ports = parse_ports(args.ports)

    console.print(f"\n[bold yellow][*] Initiating scan against target:[/bold yellow] [bold green]{target}[/bold green]")
    console.print(f"[bold dim][*] Selected port scope: {len(target_ports)} ports[/bold dim]")
    
    # 1. Run Async Port Scan with parsed target_ports
    raw_scan_results = await run_async_scan(target, target_ports)
    
    if not raw_scan_results:
        console.print("[bold red][!] No open ports detected or target unreachable.[/]")
        return

   # 2. Enrich with Service Fingerprinting (Async Probing)
    enriched_ports = []
    for item in raw_scan_results:
        service_info = await enrich_service_banner(target, item["port"], item.get("banner", ""))
        enriched_ports.append(service_info)

    console.print("\n")
    console.print(build_port_table(enriched_ports))

    # 3. Vulnerability Correlation Engine
    vulnerabilities = await analyze_vulnerabilities(raw_scan_results, target)
    
    if vulnerabilities:
        console.print("\n")
        console.print(build_vuln_table(vulnerabilities))
    else:
        console.print("\n[bold green][+] No direct vulnerability correlation matches found for detected ports.[/]")

    # 4. Generate Reports
    html_report_file = save_report(target, enriched_ports, vulnerabilities)
    console.print(f"\n[bold cyan][+] HTML Dashboard Report generated:[/] [bold underline]{html_report_file}[/]\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red][!] Scan aborted by user.[/]")
        sys.exit(0)