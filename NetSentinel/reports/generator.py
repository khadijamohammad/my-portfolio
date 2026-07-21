import os
from datetime import datetime
from typing import List, Dict, Any


def generate_html_report(target: str, scan_results: List[Dict[str, Any]], vulnerabilities: List[Dict[str, Any]], timestamp: str) -> str:
    """
    Generates a styled HTML security report and saves it to the reports folder.
    Returns the file path of the generated report.
    """
    # Count severities
    counts = {"Critical": 0, "High": 0, "Medium": 0, "Info": 0}
    for v in vulnerabilities:
        sev = v.get("severity", "Info")
        if sev in counts:
            counts[sev] += 1
        else:
            counts["Info"] += 1

    # Format scan rows
    rows_html = ""
    for item in scan_results:
        banner = item.get("banner") or "None"
        rows_html += f"""
        <tr>
            <td><strong>{item['port']}</strong></td>
            <td><span class="badge service">Active</span></td>
            <td><code>{banner}</code></td>
        </tr>
        """

    # Format vulnerability rows
    vuln_rows_html = ""
    if not vulnerabilities:
        vuln_rows_html = '<tr><td colspan="5" style="text-align:center; color:#2ecc71;">No vulnerability correlation risks identified.</td></tr>'
    else:
        for v in vulnerabilities:
            sev_class = v.get("severity", "info").lower()
            vuln_rows_html += f"""
            <tr>
                <td><span class="badge {sev_class}">{v.get('severity', 'INFO')}</span></td>
                <td><code>{v.get('cve', 'N/A')}</code></td>
                <td>{v.get('description', 'N/A')}</td>
                <td>-</td>
                <td>Review service configuration and apply latest patches.</td>
            </tr>
            """

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
            <div class="card crit-card"><h3>{counts['Critical']}</h3><p>CRITICAL</p></div>
            <div class="card high-card"><h3>{counts['High']}</h3><p>HIGH</p></div>
            <div class="card med-card"><h3>{counts['Medium']}</h3><p>MEDIUM</p></div>
            <div class="card info-card"><h3>{counts['Info']}</h3><p>INFO / LOW</p></div>
        </div>

        <h2>Network Reconnaissance & Services</h2>
        <table>
            <thead>
                <tr><th>Port</th><th>Status</th><th>Banner Details</th></tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <h2>Vulnerability Findings & Remediation</h2>
        <table>
            <thead>
                <tr><th>Severity</th><th>ID</th><th>Title / Description</th><th>Port</th><th>Remediation Action</th></tr>
            </thead>
            <tbody>
                {vuln_rows_html}
            </tbody>
        </table>
    </div>
</body>
</html>
"""

    # Save to file
    os.makedirs("reports", exist_ok=True)
    clean_target = target.replace(".", "_")
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reports/scan_report_{clean_target}_{time_str}.html"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    return filename