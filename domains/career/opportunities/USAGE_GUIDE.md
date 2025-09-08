# Opportunity Management System - Usage Guide

## Quick Start

### 1. Create a New Opportunity
```bash
python3 automation/scripts/opportunity_manager.py create "Opportunity Name" "Type" "Source" --deadline "YYYY-MM-DD" --priority "High"
```

**Example**:
```bash
python3 automation/scripts/opportunity_manager.py create "Senior Product Manager Role at TechCorp" "Employment" "LinkedIn message from recruiter" --deadline "2024-12-15" --priority "High"
```

### 2. Evaluate an Opportunity
```bash
python3 automation/scripts/opportunity_manager.py evaluate "opportunity-id" --scores '{"career_growth": 8, "financial_impact": 7, ...}'
```

**Example**:
```bash
python3 automation/scripts/opportunity_manager.py evaluate "senior-product-manager-role-at-techcorp-20250905-1315" --scores '{"career_growth": 8, "financial_impact": 7, "learning_opportunity": 6, "network_expansion": 7, "fairness": 8, "freedom": 6, "sustainability": 7, "current_capacity": 5, "opportunity_cost": 6, "market_timing": 8, "life_stage_fit": 7}'
```

### 3. List All Opportunities
```bash
python3 automation/scripts/opportunity_manager.py list
```

### 4. Check Upcoming Deadlines
```bash
python3 automation/scripts/opportunity_manager.py deadlines
```

### 5. Archive an Opportunity
```bash
python3 automation/scripts/opportunity_manager.py archive "opportunity-id" "Accepted/Declined/Passed" --notes "Reason for decision"
```

## Detailed Workflow

### Step 1: Opportunity Identification
When you learn about a new opportunity:

1. **Quick Assessment**: Use the quick assessment template to determine if it's worth pursuing
2. **Create Opportunity**: If it passes initial screening, create a new opportunity record
3. **Gather Information**: Collect all relevant documents and contact information

### Step 2: Information Gathering
1. **Contact Management**: Create contact records for all key stakeholders
2. **Document Collection**: Gather job descriptions, contracts, company information
3. **Research**: Learn about the company, role, and market context

### Step 3: Evaluation
1. **Complete Evaluation**: Use the evaluation framework to score the opportunity
2. **Decision Analysis**: Apply the 10/10/10 rule and reversibility assessment
3. **Risk Assessment**: Identify and plan for potential risks

### Step 4: Decision & Negotiation
1. **Make Decision**: Based on evaluation scores and analysis
2. **Negotiate Terms**: If proceeding, negotiate compensation and conditions
3. **Create Offers**: Document your proposals and counter-offers

### Step 5: Follow-up & Learning
1. **Track Outcomes**: Monitor results and outcomes
2. **Update Records**: Keep opportunity records current
3. **Learn & Improve**: Update evaluation criteria based on experience

## Evaluation Framework

### Scoring System
Each opportunity is evaluated across three dimensions:

#### Goals Alignment (40% weight)
- **Career Growth** (1-10): How this advances your career
- **Financial Impact** (1-10): Financial implications
- **Learning Opportunity** (1-10): Skills/knowledge gained
- **Network Expansion** (1-10): Professional network growth

#### Values Alignment (35% weight)
- **Fairness** (1-10): Fairness of terms and relationships
- **Freedom** (1-10): Impact on your autonomy
- **Sustainability** (1-10): Long-term sustainability alignment

#### Timing & Logistics (25% weight)
- **Current Capacity** (1-10): Time/energy availability
- **Opportunity Cost** (1-10): What you're giving up
- **Market Timing** (1-10): Right time for this opportunity
- **Life Stage Fit** (1-10): Fits current life priorities

### Score Interpretation
- **90-100**: Exceptional opportunity - Strong yes
- **80-89**: Very good opportunity - Likely yes
- **70-79**: Good opportunity - Consider carefully
- **60-69**: Moderate opportunity - Proceed with caution
- **50-59**: Poor opportunity - Likely no
- **Below 50**: Very poor opportunity - Strong no

## File Structure

### Individual Opportunity Folder
```
active/[opportunity-id]/
├── overview.md          # Opportunity summary and details
├── evaluation.md        # Evaluation scores and analysis
├── timeline.md          # Decision timeline and milestones
├── metadata.json        # System metadata and scores
├── documents/           # Related documents
├── contacts/            # Contact information
└── offers/              # Your proposals and offers
```

### Templates
- `templates/opportunity_template.md` - Complete opportunity template
- `templates/quick_assessment.md` - Rapid initial evaluation
- `templates/contact_template.md` - Contact management
- `templates/offer_template.md` - Proposal documentation

## Best Practices

### Opportunity Creation
- Use descriptive names that clearly identify the opportunity
- Set realistic deadlines based on the decision timeline
- Assign appropriate priority levels
- Include all relevant source information

### Evaluation Process
- Be honest and objective in your scoring
- Consider both short-term and long-term implications
- Consult with trusted advisors for important decisions
- Document your reasoning for future reference

### Contact Management
- Create contact records for all key stakeholders
- Track relationship history and interaction notes
- Update contact information regularly
- Maintain professional relationships

### Document Organization
- Keep all related documents in the opportunity folder
- Use consistent naming conventions
- Regularly update documents as information changes
- Archive completed opportunities properly

## Automation Features

### Automated Scoring
- The system automatically calculates weighted scores
- Provides recommendations based on total scores
- Updates evaluation files with calculated results

### Deadline Tracking
- Monitors upcoming decision deadlines
- Provides alerts for opportunities requiring attention
- Helps prioritize evaluation efforts

### Metadata Management
- Tracks opportunity status and progress
- Maintains evaluation history
- Provides summary views of all opportunities

## Integration with Personal System

### Goals Alignment
- Links to your personal goals in `core/identity/goals.md`
- Evaluates opportunities against your long-term vision
- Considers career development objectives

### Values Alignment
- References your core values in `core/identity/values.md`
- Ensures opportunities align with your principles
- Maintains consistency with your decision-making framework

### Decision Making
- Uses your decision-making principles from `core/principles/decision_making.md`
- Applies the 10/10/10 rule and reversibility assessment
- Integrates with your overall decision-making process

## Troubleshooting

### Common Issues

#### Python Command Not Found
```bash
# Use python3 instead of python
python3 automation/scripts/opportunity_manager.py [command]
```

#### Permission Errors
```bash
# Make script executable
chmod +x automation/scripts/opportunity_manager.py
```

#### Missing Dependencies
```bash
# Install required packages
pip3 install pyyaml
```

### Getting Help
- Check the README files in each directory
- Review the evaluation framework documentation
- Use the template files as examples
- Consult the automation script help: `python3 automation/scripts/opportunity_manager.py --help`

## Examples

### Example 1: Job Opportunity
```bash
# Create opportunity
python3 automation/scripts/opportunity_manager.py create "Product Manager at StartupCo" "Employment" "Referral from John Smith" --deadline "2024-12-20" --priority "High"

# Evaluate opportunity
python3 automation/scripts/opportunity_manager.py evaluate "product-manager-at-startupco-20250905-1400" --scores '{"career_growth": 9, "financial_impact": 6, "learning_opportunity": 8, "network_expansion": 7, "fairness": 8, "freedom": 7, "sustainability": 6, "current_capacity": 6, "opportunity_cost": 5, "market_timing": 8, "life_stage_fit": 7}'
```

### Example 2: Consulting Opportunity
```bash
# Create opportunity
python3 automation/scripts/opportunity_manager.py create "Digital Transformation Consulting" "Consulting" "Cold outreach from client" --deadline "2024-12-10" --priority "Medium"

# Evaluate opportunity
python3 automation/scripts/opportunity_manager.py evaluate "digital-transformation-consulting-20250905-1400" --scores '{"career_growth": 6, "financial_impact": 8, "learning_opportunity": 7, "network_expansion": 6, "fairness": 7, "freedom": 9, "sustainability": 7, "current_capacity": 8, "opportunity_cost": 4, "market_timing": 7, "life_stage_fit": 8}'
```

## Regular Maintenance

### Weekly Tasks
- [ ] Review all active opportunities
- [ ] Update status and progress
- [ ] Check upcoming deadlines
- [ ] Follow up on pending actions

### Monthly Tasks
- [ ] Archive completed opportunities
- [ ] Review evaluation criteria
- [ ] Update contact information
- [ ] Analyze patterns and trends

### Quarterly Tasks
- [ ] Comprehensive system review
- [ ] Update templates and frameworks
- [ ] Analyze success rates and outcomes
- [ ] Refine evaluation criteria

---
*Usage guide created: [Date]*
*Last updated: [Date]*
