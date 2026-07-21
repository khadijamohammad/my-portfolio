import os
import json
from datetime import datetime

def generate_html_report(target: str, enriched_ports: list, vulnerabilities: list, timestamp: str) -> str:
    """Generates a clean HTML dashboard string for scan findings."""
    
    # Count severity totals
    crit_count = sum(1 for v in vulnerabilities if v.get("severity") == "CRITICAL")
    high_count = sum(1 for v in vulnerabilities if v.get("severity") == "HIGH")
    med_count = sum(1 for v in vulnerabilities if v.get("severity") == "MEDIUM")
    low_count = sum(1 for v in vulnerabilities if v.get("severity") in ["LOW", "INFO"])

    # Build Port Rows
    port_rows = ""
    for p in enriched_ports:
        port_rows += f"""
        <tr>
            <td><strong>{p.get('port')}</strong></td>
            <td><span class="badge service">{p.get('service')}</span></td>
            <td><code>{p.get('banner_details')}</code></td>
        </tr>
        """

    # Build Vulnerability Rows
    vuln_rows = ""
    if vulnerabilities:
        for v in vulnerabilities:
            sev = v.get("severity", "INFO")
            sev_class = sev.lower()
            vuln_rows += f"""
            <tr>
                <td><span class="badge {sev_class}">{sev}</span></td>
                <td><strong>{v.get('cve_id')}</strong></td>
                <td>{v.get('title')}</td>
                <td>Port {v.get('matched_port')}</td>
                <td><small>{v.get('remediation', 'N/A')}</small></td>
            </tr>
            """
    else:
        vuln_rows = '<tr><td colspan="5" style="text-align:center; color:#2ecc71;">No vulnerability correlation risks identified.</td></tr>'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NetSentinel Scan Report - {target}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 30px; }}
        .container {{ max-width: 1000px; margin: auto; }}
        .header {{ background: #1e293b; padding: 25px; border-radius: 10px; border-left: 6px solid #38bdf8; margin-bottom: 25px; }}
        h1 {{ margin: 0 0 10px 0; font-size: 24px; color: #38bdf8; }}
        .meta {{ color: #94a3b8; font-size: 14px; }}
        
        .stats {{ display: flex; gap: 15px; margin-bottom: 25px; }}
        .card {{ flex: 1; background: #1e293b; padding: 15px; border-radius: 8px; text-align: center; }}
        .card h3 {{ margin: 0; font-size: 28px; }}
        .card p {{ margin: 5px 0 0 0; color: #94a3b8; font-size: 12px; font-weight: bold; }}
        
        .crit-card h3 {{ color: #ef4444; }}
        .high-card h3 {{ color: #f97316; }}
        .med-card h3 {{ color: #eab308; }}
        .info-card h3 {{ color: #3b82f6; }}
        
        table {{ width: 100%; border-collapse: collapse; background: #1e293b; border-radius: 8px; overflow: hidden; margin-bottom: 30px; }}
        th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid #334155; font-size: 14px; }}
        th {{ background: #0f172a; color: #94a3b8; text-transform: uppercase; font-size: 12px; letter-spacing: 0.5px; }}
        
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block; }}
        .badge.critical {{ background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; }}
        .badge.high {{ background: rgba(249, 115, 22, 0.2); color: #f97316; border: 1px solid #f97316; }}
        .badge.medium {{ background: rgba(234, 179, 8, 0.2); color: #eab308; border: 1px solid #eab308; }}
        .badge.info {{ background: rgba(59, 130, 246, 0.2); color: #3b82f6; border: 1px solid #3b82f6; }}
        .badge.service {{ background: #334155; color: #38bdf8; }}
        code {{ background: #0f172a; padding: 2px 6px; border-radius: 4px; color: #a5f3fc; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ NetSentinel Security Dashboard</h1>
            <div class="meta">Target: <strong>{target}</strong> | Generated: {timestamp}</div>
        </div>

        <div class="stats">
            <div class="card crit-card"><h3>{crit_count}</h3><p>CRITICAL</p></div>
            <div class="card high-card"><h3>{high_count}</h3><p>HIGH</p></div>
            <div class="card med-card"><h3>{med_count}</h3><p>MEDIUM</p></div>
            <div class="card info-card"><h3>{low_count}</h3><p>INFO / LOW</p></div>
        </div>

        <h2>Network Reconnaissance & Services</h2>
        <table>
            <thead>
                <tr><th>Port</th><th>Service</th><th>Banner Details</th></tr>
            </thead>
            <tbody>
                {port_rows}
            </tbody>
        </table>

        <h2>Vulnerability Findings & Remediation</h2>
        <table>
            <thead>
                <tr><th>Severity</th><th>ID</th><th>Title</th><th>Port</th><th>Remediation Action</th></tr>
            </thead>
            <tbody>
                {vuln_rows}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
    return html_content


def save_report(target: str, enriched_ports: list, vulnerabilities: list, reports_dir: str = "reports") -> str:
    """Saves both JSON raw data and an HTML dashboard report."""
    os.makedirs(reports_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_target = target.replace(".", "_").replace(":", "_")

    # 1. Save JSON Report
    json_path = os.path.join(reports_dir, f"scan_report_{safe_target}_{timestamp}.json")
    report_data = {
        "target": target,
        "timestamp": formatted_time,
        "ports": enriched_ports,
        "vulnerabilities": vulnerabilities
    }
    with open(json_path, "w") as f:
        json.dump(report_data, f, indent=4)

    # 2. Save HTML Dashboard Report
    html_path = os.path.join(reports_dir, f"scan_report_{safe_target}_{timestamp}.html")
    html_content = generate_html_report(target, enriched_ports, vulnerabilities, formatted_time)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return html_path