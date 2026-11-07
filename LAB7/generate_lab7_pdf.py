import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8.5)
        self.setFillColor(colors.HexColor("#718096"))
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "SE Lab 7: Fuzzing for Input Validation Bugs")
            self.drawRightString(558, 755, "PES1UG24CS478 — Sujay Hegde")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.8)
            self.line(54, 747, 558, 747)
        # Footer
        self.setFont("Helvetica", 8.5)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "PES University | Department of Computer Science & Engineering")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.8)
        self.line(54, 46, 558, 46)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=10
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#2B6CB0'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14.5,
        textColor=colors.HexColor('#2D3748'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=5
    )
    bold_body = ParagraphStyle(
        'BoldBody_Custom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    code_inline = ParagraphStyle(
        'CodeInline',
        parent=body_style,
        fontName='Courier',
        fontSize=8.5,
        textColor=colors.HexColor('#6B46C1')
    )
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#2C5282'),
        spaceAfter=8
    )

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("LAB 7: Fuzzing for Input Validation Bugs", title_style))
    story.append(Paragraph("Software Engineering Lab Report &amp; Reflection Analysis", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2B6CB0'), spaceAfter=10))

    # Student Info Table
    info_data = [
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Sujay Hegde", body_style),
         Paragraph("<b>SRN / Roll No:</b>", body_style), Paragraph("PES1UG24CS478", body_style)],
        [Paragraph("<b>Course:</b>", body_style), Paragraph("Software Engineering (SE)", body_style),
         Paragraph("<b>Semester / Sec:</b>", body_style), Paragraph("6th Sem / CSE", body_style)],
        [Paragraph("<b>Repository:</b>", body_style), Paragraph("sujayhegde23/LAB6-LAB7-SE-PES1UG24CS478", body_style),
         Paragraph("<b>Lab Duration:</b>", body_style), Paragraph("60 minutes", body_style)]
    ]
    info_table = Table(info_data, colWidths=[95, 155, 95, 159])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("1. Objective &amp; Theoretical Background", h1_style))
    story.append(Paragraph(
        "<b>Objective:</b> To explore fuzz testing as a dynamic security and quality assurance technique by "
        "identifying and fixing input validation bugs in a museum admission parser module using the Python "
        "<b>Hypothesis</b> property-based fuzzing framework.",
        body_style
    ))
    story.append(Paragraph(
        "<b>What is Fuzz Testing?</b> Fuzzing feeds unexpected, malformed, or boundary-case data into a program "
        "to discover unhandled exceptions, logical bugs, and vulnerabilities before deployment. "
        "While traditional unit tests check only known, anticipated inputs, property-based testing with Hypothesis "
        "allows developers to define high-level invariants (e.g. <i>'the parser must never crash regardless of input'</i>) "
        "and automatically generates hundreds of randomized test cases to actively falsify those invariants.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. Step 2 — Initial Run of the Buggy Application (SS1)", h1_style))
    story.append(Paragraph(
        "The module <code>museum_admission_parser.py</code> provides three parsing routines: "
        "<code>format_visitor_name(name)</code>, <code>parse_group_ages(text)</code>, and "
        "<code>parse_visit_date(text)</code>. On valid happy-path inputs, the script completes successfully:",
        body_style
    ))
    story.append(Image("c:/se/LAB6-LAB7/LAB7/SS1_buggy_run.png", width=6.5*inch, height=2.85*inch))
    story.append(Paragraph("<b>Screenshot SS1:</b> Running <code>python museum_admission_parser.py</code> on the buggy module with happy-path inputs.", callout_style))

    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph("3. Step 3 &amp; 4 — Hypothesis Fuzz Testing &amp; Failures (SS2)", h1_style))
    story.append(Paragraph(
        "In <code>test_museum_admission_parser.py</code>, we implemented property-based tests using the "
        "<code>@given(st.text() | st.none())</code> strategy with try-except assertion wrappers. "
        "Executing <code>pytest test_museum_admission_parser.py</code> immediately triggered crashes in all three functions:",
        body_style
    ))

    bugs_table_data = [
        [Paragraph("<b>Function Under Test</b>", bold_body), Paragraph("<b>Failing Inputs Found</b>", bold_body), Paragraph("<b>Exception Raised</b>", bold_body), Paragraph("<b>Vulnerability Root Cause</b>", bold_body)],
        [Paragraph("<code>format_visitor_name</code>", code_inline), Paragraph("<code>None</code><br/><code>''</code> (empty)<br/><code>' '</code> (spaces)", body_style), Paragraph("<code>AttributeError</code><br/><code>IndexError</code>", body_style), Paragraph("Called <code>.split()</code> on None; accessed <code>parts[-1]</code> on an empty list.", body_style)],
        [Paragraph("<code>parse_group_ages</code>", code_inline), Paragraph("<code>None</code><br/><code>'abc'</code><br/><code>'12.5'</code>", body_style), Paragraph("<code>AttributeError</code><br/><code>ValueError</code>", body_style), Paragraph("Called <code>.split()</code> on None; unhandled <code>int()</code> parse error on non-integers.", body_style)],
        [Paragraph("<code>parse_visit_date</code>", code_inline), Paragraph("<code>None</code><br/><code>''</code><br/><code>'2026-11'</code>", body_style), Paragraph("<code>AttributeError</code><br/><code>ValueError</code>", body_style), Paragraph("Called <code>.strip()</code> on None; unpacked sequence with invalid delimiter count.", body_style)],
    ]
    bugs_table = Table(bugs_table_data, colWidths=[120, 110, 105, 169])
    bugs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E0')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(bugs_table)
    story.append(Spacer(1, 10))

    story.append(Image("c:/se/LAB6-LAB7/LAB7/SS2_tests_failing.png", width=6.5*inch, height=3.55*inch))
    story.append(Paragraph("<b>Screenshot SS2:</b> <code>pytest test_museum_admission_parser.py</code> failing on the buggy module with minimized Hypothesis counterexamples.", callout_style))

    story.append(PageBreak())

    # ================= PAGE 3 =================
    story.append(Paragraph("4. Step 5 — Defensive Programming Fixes Applied (SS3)", h1_style))
    story.append(Paragraph(
        "To make the parser completely robust against any input generated during fuzzing, we applied defensive programming:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Type &amp; Null Guard Clauses:</b> Verified <code>if not s or not isinstance(s, str)</code> upfront before string operations, safely returning default fallbacks (<code>''</code>, <code>[]</code>, or <code>None</code>).<br/>"
        "• <b>Precondition &amp; Length Validation:</b> Checked token list lengths before indexing (e.g. <code>if not parts</code>, <code>if len(parts) == 1</code>) to prevent <code>IndexError</code> and handle single-word names gracefully.<br/>"
        "• <b>Exception Containment for Conversions:</b> Wrapped integer conversions in <code>try...except (ValueError, TypeError)</code> and filtered out invalid tokens, floats, or negative numbers.<br/>"
        "• <b>Calendar Range Verification:</b> Verified date tokens using <code>datetime.date(year, month, day)</code> to reject out-of-range dates (e.g. Feb 30, Month 13) and integer overflow safely.",
        body_style
    ))
    story.append(Spacer(1, 6))
    story.append(Image("c:/se/LAB6-LAB7/LAB7/SS3_fixed_run.png", width=6.5*inch, height=2.85*inch))
    story.append(Paragraph("<b>Screenshot SS3:</b> Running <code>python museum_admission_parser.py</code> on the hardened module.", callout_style))

    story.append(PageBreak())

    # ================= PAGE 4 =================
    story.append(Paragraph("5. Step 6 — Re-running Fuzz Tests on Fixed Module (SS4)", h1_style))
    story.append(Paragraph(
        "We re-ran <code>pytest test_museum_admission_parser.py -v</code> against the hardened parser. "
        "Hypothesis generated hundreds of randomized unicode strings, nulls, special characters, and boundary inputs. "
        "<b>All 3 property-based test suites passed with 100% success rate:</b>",
        body_style
    ))
    story.append(Image("c:/se/LAB6-LAB7/LAB7/SS4_tests_passing.png", width=6.5*inch, height=2.85*inch))
    story.append(Paragraph("<b>Screenshot SS4:</b> All 3 Hypothesis property-based fuzz tests passing cleanly on the hardened parser module.", callout_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("6. Answers to Lab 7 Reflection Questions", h1_style))
    story.append(Paragraph("<b>Reflection Question 1: What types of bugs or edge cases did Hypothesis uncover that traditional manual or unit tests often miss?</b>", h2_style))
    story.append(Paragraph(
        "<b>Answer:</b> Manual unit tests are predominantly written to verify expected operational scenarios ('happy paths'). "
        "Hypothesis systematically generated and exposed several edge cases that developer-written tests overlook:<br/>"
        "1. <b>Null Inputs (<code>None</code>):</b> Python's dynamic typing allows passing <code>None</code>, causing immediate <code>AttributeError</code> when invoking methods like <code>.split()</code> or <code>.strip()</code>.<br/>"
        "2. <b>Empty and Purely Whitespace Strings:</b> Strings such as <code>''</code> or <code>'   '</code> produce empty lists when split, resulting in <code>IndexError: list index out of range</code> when accessing <code>parts[-1]</code>.<br/>"
        "3. <b>Malformed Delimiters &amp; Unpacking Mismatches:</b> Date strings lacking or exceeding two hyphens (e.g., <code>'2026-11'</code> or <code>'2026-11-05-01'</code>) caused <code>ValueError</code> on tuple unpacking.<br/>"
        "4. <b>Type Conversion Explosions:</b> Non-numeric or floating-point age tokens (e.g. <code>'abc'</code>, <code>'12.5'</code>) caused unhandled <code>ValueError</code> in integer conversions.<br/>"
        "5. <b>Calendar Invalid Dates:</b> Syntactically matching dates that violate calendar rules (e.g. <code>2026-02-30</code> or <code>2026-13-45</code>) were caught and properly invalidated.",
        body_style
    ))

    story.append(PageBreak())

    # ================= PAGE 5 =================
    story.append(Paragraph("6. Answers to Lab 7 Reflection Questions (Continued)", h1_style))
    story.append(Paragraph("<b>Reflection Question 2: How does property-based testing (fuzzing) differ fundamentally from traditional example-based unit testing?</b>", h2_style))
    story.append(Paragraph(
        "<b>Answer:</b> The fundamental differences lie in input scope, assertion philosophy, and failure minimization:<br/>"
        "• <b>Input Generation:</b> Example-based unit tests evaluate specific, developer-chosen input-output pairs ($f(x) == y$). "
        "Property-based testing uses strategies (such as <code>st.text() | st.none()</code>) to autonomously synthesize hundreds to thousands of diverse, pseudorandom inputs, including unexpected boundary values.<br/>"
        "• <b>Verification Criteria:</b> Traditional tests check concrete values. Property-based tests verify <i>universal system invariants</i>—rules that must remain true across the entire domain of inputs (e.g., <i>'The parser must never crash or raise unhandled exceptions'</i>, or <i>'Valid date inputs always produce a 3-element tuple'</i>).<br/>"
        "• <b>Automated Shrinking:</b> When Hypothesis finds an input that violates an invariant, it automatically performs test-case reduction (shrinking) to find the smallest, simplest counterexample (e.g., shrinking a large corrupted string down to <code>''</code> or <code>None</code>), drastically simplifying debugging.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Reflection Question 3: What defensive programming techniques were implemented to harden the application against unexpected or malformed inputs?</b>", h2_style))
    story.append(Paragraph(
        "<b>Answer:</b> The following defensive programming principles were applied to achieve resilience:<br/>"
        "1. <b>Type Safety &amp; Guard Clauses:</b> Verified input existence and type validity (<code>isinstance(s, str)</code>) at the start of each function, returning safe, predictable defaults (<code>''</code>, <code>[]</code>, or <code>None</code>) on invalid inputs.<br/>"
        "2. <b>Precondition and Boundary Checking:</b> Inspected collection lengths before indexing or unpacking (checking <code>if not parts</code>, <code>if len(parts) == 1</code>, and <code>len(parts) == 3</code>) to prevent <code>IndexError</code> and <code>ValueError</code>.<br/>"
        "3. <b>Exception Containment:</b> Wrapped type-casting operations in targeted <code>try...except (ValueError, TypeError)</code> blocks, allowing graceful token filtering instead of fatal crashes.<br/>"
        "4. <b>Semantic &amp; Domain Validation:</b> Employed the Python standard library's <code>datetime.date()</code> to validate calendar correctness and reject overflow or out-of-range dates safely.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {filename}")

if __name__ == "__main__":
    pdf_primary = "c:/se/LAB6-LAB7/LAB7/PES1UG24CS478_Sujay_Hegde_LAB7.pdf"
    pdf_alias = "c:/se/LAB6-LAB7/LAB7/PES1UG24CS478_LAB7.pdf"
    build_pdf(pdf_primary)
    build_pdf(pdf_alias)
