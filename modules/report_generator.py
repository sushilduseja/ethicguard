def generate_report(bias_result, pii_result):
    """Generate a text-based report with findings and recommendations."""
    report = "EthicGuard Assessment Report\n"
    report += "=" * 30 + "\n\n"
    report += "**Bias Detection**\n"
    report += f"{bias_result}\n"
    report += "See the bias visualization chart for a comparison of group means.\n\n"
    report += "**Privacy Check**\n"
    report += f"{pii_result}\n\n"
    report += "**Recommendations**\n"
    if "Potential bias detected" in bias_result:
        report += "- Investigate and mitigate bias in identified groups.\n"
    if "PII found" in pii_result:
        report += "- Remove or anonymize PII to ensure privacy.\n"
    if "No significant bias" in bias_result and "No PII detected" in pii_result:
        report += "- No immediate issues found. Continue monitoring.\n"
    return report