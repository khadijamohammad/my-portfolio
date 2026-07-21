import argparse
import asyncio
import logging
import sys
from datetime import datetime
from typing import List, Dict, Any
from core.scanner import run_scan
from reports.generator import generate_html_report

# Configure structured logging format
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)


def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments for target and ports."""
    parser = argparse.ArgumentParser(
        description="NetSentinel - Async Network Scanner & Service Recon Engine"
    )
    parser.add_argument(
        "--target",
        type=str,
        default="127.0.0.1",
        help="Target IP address (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--ports",
        type=str,
        default="21,22,80,135,443,445,8080",
        help="Comma-separated list of ports to scan"
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_arguments()
    
    try:
        port_list: List[int] = [int(p.strip()) for p in args.ports.split(",")]
    except ValueError:
        logging.error("Invalid port list provided. Please supply integers separated by commas.")
        sys.exit(1)

    logging.info(f"Starting NetSentinel engine against target: {args.target}")
    logging.info(f"Scanning {len(port_list)} designated ports...")

    scan_results = await run_scan(args.target, port_list)

    logging.info(f"Scan complete. Found {len(scan_results)} open port(s).")
    
    # Collect all discovered vulnerabilities into a single list
    all_vulnerabilities: List[Dict[str, Any]] = []
    for item in scan_results:
        banner_info = f" | Banner: {item['banner']}" if item.get("banner") else ""
        logging.info(f" -> Port {item['port']}: OPEN{banner_info}")
        if item.get("vulnerabilities"):
            for vuln in item["vulnerabilities"]:
                all_vulnerabilities.append(vuln)
                logging.warning(f"    [!] Risk: {vuln['severity']} - {vuln['description']}")

    # Generate timestamp and invoke report generator
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_path = generate_html_report(args.target, scan_results, all_vulnerabilities, timestamp)
    logging.info(f"Report successfully written to: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())