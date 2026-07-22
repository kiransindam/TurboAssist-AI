"""Create sample PDF documents for testing."""
from fpdf import FPDF
from pathlib import Path


def create_sample_pdf(file_path: str, title: str, content: list):
    """Create a sample PDF with technical content."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    for section in content:
        pdf.multi_cell(0, 10, section)
        pdf.ln(5)
    
    pdf.output(file_path)


def main():
    """Create sample technical documents."""
    data_dir = Path("data/sample_docs")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample 1: SGT-800 Maintenance Manual
    sgt800_content = [
        "SGT-800 Gas Turbine Maintenance Manual\n\n",
        "Chapter 1: Introduction\n",
        "The SGT-800 is an industrial gas turbine designed for power generation and mechanical drive applications. This manual provides comprehensive maintenance procedures and troubleshooting guidelines.\n\n",
        "Chapter 2: Maintenance Intervals\n",
        "Recommended maintenance intervals:\n",
        "- Basic inspection: Every 8,000 operating hours\n",
        "- Major inspection: Every 25,000 operating hours or 5 years\n",
        "- Hot gas path inspection: Every 15,000 operating hours\n",
        "- Combustion inspection: Every 8,000 operating hours\n\n",
        "Chapter 3: Vibration Troubleshooting\n",
        "Excessive vibration may indicate:\n",
        "1. Rotor imbalance - Check balance weights and rotor alignment\n",
        "2. Bearing wear - Inspect bearing clearances and lubrication\n",
        "3. Misalignment - Verify coupling alignment within 0.05mm tolerance\n",
        "4. Blade damage - Inspect compressor and turbine blades\n\n",
        "Vibration limits:\n",
        "- Normal operation: < 2.5 mm/s RMS\n",
        "- Alert threshold: 4.5 mm/s RMS\n",
        "- Trip threshold: 7.0 mm/s RMS\n\n",
        "Chapter 4: Safety Procedures\n",
        "Before any maintenance work:\n",
        "1. Implement lockout/tagout (LOTO) procedures\n",
        "2. Verify zero energy state\n",
        "3. Obtain required permits (hot work, confined space)\n",
        "4. Wear appropriate PPE: hard hat, safety glasses, steel-toe boots, hearing protection\n",
        "5. Ensure proper ventilation in enclosed spaces\n",
        "6. Have fire extinguisher readily available\n\n",
        "Chapter 5: Lubrication System\n",
        "The lubrication system requires:\n",
        "- Oil type: ISO VG 46 turbine oil\n",
        "- Oil capacity: 450 liters\n",
        "- Oil change interval: Every 8,000 hours or annually\n",
        "- Oil temperature range: 40-60°C during operation\n",
        "- Filter replacement: Every 4,000 hours\n"
    ]
    
    create_sample_pdf(
        str(data_dir / "SGT800_Maintenance_Manual.pdf"),
        "SGT-800 Gas Turbine Maintenance Manual",
        sgt800_content
    )
    
    # Sample 2: SST-900 Steam Turbine Guide
    sst900_content = [
        "SST-900 Steam Turbine Operations Guide\n\n",
        "Chapter 1: Overview\n",
        "The SST-900 is a high-efficiency steam turbine suitable for combined cycle power plants and industrial applications.\n\n",
        "Chapter 2: Startup Procedures\n",
        "Cold startup sequence:\n",
        "1. Verify all systems are in safe state\n",
        "2. Establish lube oil circulation (minimum 30 minutes)\n",
        "3. Warm up steam lines gradually (rate: 50°C/hour)\n",
        "4. Roll turbine at 500 RPM for 15 minutes\n",
        "5. Accelerate to rated speed (3000/3600 RPM)\n",
        "6. Synchronize to grid\n",
        "7. Load ramp to minimum load (20%)\n\n",
        "Chapter 3: Common Issues\n",
        "Issue: High exhaust temperature\n",
        "Causes:\n",
        "- Fouled blading\n",
        "- Steam leak in casing\n",
        "- Instrument error\n",
        "Solution: Clean blading, inspect seals, calibrate instruments\n\n",
        "Issue: Low efficiency\n",
        "Causes:\n",
        "- Steam path deposits\n",
        "- Worn seals\n",
        "- Incorrect steam conditions\n",
        "Solution: Chemical cleaning, seal replacement, verify steam parameters\n\n",
        "Chapter 4: Maintenance Schedule\n",
        "- Daily: Visual inspection, log parameters\n",
        "- Weekly: Check oil levels, vibration readings\n",
        "- Monthly: Oil analysis, valve testing\n",
        "- Annual: Major inspection, rotor inspection\n",
        "- Every 5 years: Complete overhaul\n"
    ]
    
    create_sample_pdf(
        str(data_dir / "SST900_Operations_Guide.pdf"),
        "SST-900 Steam Turbine Operations Guide",
        sst900_content
    )
    
    print("✅ Created sample PDFs in data/sample_docs/")
    print("   - SGT800_Maintenance_Manual.pdf")
    print("   - SST900_Operations_Guide.pdf")


if __name__ == "__main__":
    main()
