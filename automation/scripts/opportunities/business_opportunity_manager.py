#!/usr/bin/env python3
"""
Business Opportunity Management System
Automated tracking, evaluation, and management of business opportunities.
"""

import os
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

class BusinessOpportunityManager:
    def __init__(self, base_path: str = None):
        """Initialize the business opportunity manager."""
        if base_path is None:
            self.base_path = Path(__file__).parent.parent.parent / "domains" / "business_opportunities"
        else:
            self.base_path = Path(base_path)
        
        self.active_path = self.base_path / "active"
        self.pipeline_path = self.base_path / "pipeline"
        self.archive_path = self.base_path / "archive"
        self.templates_path = self.base_path / "templates"
        
        # Ensure directories exist
        for path in [self.active_path, self.pipeline_path, self.archive_path, self.templates_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    def create_opportunity(self, name: str, opportunity_type: str, source: str, 
                          deadline: str = None, priority: str = "Medium") -> str:
        """Create a new business opportunity folder and files."""
        # Generate opportunity ID
        opportunity_id = self._generate_opportunity_id(name)
        opportunity_path = self.active_path / opportunity_id
        
        # Create opportunity directory structure
        opportunity_path.mkdir(exist_ok=True)
        (opportunity_path / "business_plan").mkdir(exist_ok=True)
        (opportunity_path / "documents").mkdir(exist_ok=True)
        (opportunity_path / "contacts").mkdir(exist_ok=True)
        (opportunity_path / "offers").mkdir(exist_ok=True)
        
        # Create overview.md
        overview_content = self._create_overview_template(name, opportunity_type, source, deadline, priority)
        with open(opportunity_path / "overview.md", "w") as f:
            f.write(overview_content)
        
        # Create evaluation.md
        evaluation_content = self._create_evaluation_template()
        with open(opportunity_path / "evaluation.md", "w") as f:
            f.write(evaluation_content)
        
        # Create timeline.md
        timeline_content = self._create_timeline_template(deadline)
        with open(opportunity_path / "timeline.md", "w") as f:
            f.write(timeline_content)
        
        # Create opportunity metadata
        metadata = {
            "id": opportunity_id,
            "name": name,
            "type": opportunity_type,
            "source": source,
            "status": "Evaluating",
            "priority": priority,
            "created": datetime.now().isoformat(),
            "deadline": deadline,
            "score": None
        }
        
        with open(opportunity_path / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Created business opportunity: {opportunity_id}")
        print(f"Path: {opportunity_path}")
        
        return opportunity_id
    
    def evaluate_opportunity(self, opportunity_id: str, scores: Dict[str, int]) -> Dict[str, any]:
        """Evaluate a business opportunity and calculate total score."""
        opportunity_path = self.active_path / opportunity_id
        
        if not opportunity_path.exists():
            raise ValueError(f"Business opportunity {opportunity_id} not found")
        
        # Calculate weighted scores
        business_score = (
            scores.get("market_size", 0) +
            scores.get("competitive_advantage", 0) +
            scores.get("scalability", 0) +
            scores.get("revenue_model", 0)
        )
        
        goals_score = (
            scores.get("career_growth", 0) +
            scores.get("financial_impact", 0) +
            scores.get("learning_opportunity", 0) +
            scores.get("network_expansion", 0)
        )
        
        values_score = (
            scores.get("fairness", 0) +
            scores.get("freedom", 0) +
            scores.get("sustainability", 0)
        )
        
        timing_score = (
            scores.get("current_capacity", 0) +
            scores.get("market_timing", 0) +
            scores.get("execution_risk", 0) +
            scores.get("life_stage_fit", 0)
        )
        
        total_score = business_score + goals_score + values_score + timing_score
        
        # Update metadata
        metadata_path = opportunity_path / "metadata.json"
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        
        metadata["score"] = total_score
        metadata["evaluation_date"] = datetime.now().isoformat()
        metadata["scores"] = scores
        
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Update evaluation.md
        self._update_evaluation_file(opportunity_path, scores, total_score)
        
        return {
            "opportunity_id": opportunity_id,
            "total_score": total_score,
            "business_score": business_score,
            "goals_score": goals_score,
            "values_score": values_score,
            "timing_score": timing_score,
            "recommendation": self._get_recommendation(total_score)
        }
    
    def get_opportunities_summary(self) -> List[Dict]:
        """Get summary of all active business opportunities."""
        opportunities = []
        
        for opportunity_dir in self.active_path.iterdir():
            if opportunity_dir.is_dir():
                metadata_path = opportunity_dir / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, "r") as f:
                        metadata = json.load(f)
                    opportunities.append(metadata)
        
        # Sort by priority and score
        opportunities.sort(key=lambda x: (
            {"High": 3, "Medium": 2, "Low": 1}.get(x.get("priority", "Medium"), 2),
            x.get("score", 0)
        ), reverse=True)
        
        return opportunities
    
    def check_deadlines(self) -> List[Dict]:
        """Check for business opportunities with upcoming deadlines."""
        upcoming_deadlines = []
        today = datetime.now().date()
        
        for opportunity_dir in self.active_path.iterdir():
            if opportunity_dir.is_dir():
                metadata_path = opportunity_dir / "metadata.json"
                if metadata_path.exists():
                    with open(metadata_path, "r") as f:
                        metadata = json.load(f)
                    
                    if metadata.get("deadline"):
                        deadline = datetime.fromisoformat(metadata["deadline"]).date()
                        days_until = (deadline - today).days
                        
                        if 0 <= days_until <= 7:  # Within next week
                            upcoming_deadlines.append({
                                **metadata,
                                "days_until_deadline": days_until
                            })
        
        return sorted(upcoming_deadlines, key=lambda x: x["days_until_deadline"])
    
    def archive_opportunity(self, opportunity_id: str, status: str, notes: str = ""):
        """Archive a business opportunity with final status."""
        opportunity_path = self.active_path / opportunity_id
        archive_path = self.archive_path / opportunity_id
        
        if not opportunity_path.exists():
            raise ValueError(f"Business opportunity {opportunity_id} not found")
        
        # Update metadata
        metadata_path = opportunity_path / "metadata.json"
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        
        metadata["status"] = status
        metadata["archived_date"] = datetime.now().isoformat()
        metadata["archive_notes"] = notes
        
        # Move to archive
        archive_path.mkdir(exist_ok=True)
        for item in opportunity_path.iterdir():
            if item.is_file():
                item.rename(archive_path / item.name)
            elif item.is_dir():
                (archive_path / item.name).mkdir(exist_ok=True)
                for subitem in item.iterdir():
                    subitem.rename(archive_path / item.name / subitem.name)
        
        # Remove original directory
        opportunity_path.rmdir()
        
        print(f"Archived business opportunity {opportunity_id} with status: {status}")
    
    def _generate_opportunity_id(self, name: str) -> str:
        """Generate a unique business opportunity ID."""
        # Clean name and create ID
        clean_name = "".join(c.lower() for c in name if c.isalnum() or c in " -_")
        clean_name = clean_name.replace(" ", "-").replace("_", "-")
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        return f"{clean_name}-{timestamp}"
    
    def _create_overview_template(self, name: str, opportunity_type: str, 
                                 source: str, deadline: str, priority: str) -> str:
        """Create overview template content."""
        return f"""# Business Opportunity: {name}

## Basic Information
**Date Created**: {datetime.now().strftime("%Y-%m-%d")}
**Status**: 🔍 Evaluating
**Type**: {opportunity_type}
**Priority**: {priority}
**Source**: {source}

## Opportunity Summary
**Company/Project**: [Name]
**Industry/Sector**: [Industry]
**Stage**: Idea | MVP | Early Stage | Growth | Mature
**Location**: [Geographic location]
**Team Size**: [Number of people]
**Funding Status**: [Funding stage and amount]

## Business Overview
**Problem Statement**: [What problem does this solve?]
**Solution**: [How does this solve the problem?]
**Target Market**: [Who are the customers?]
**Business Model**: [How does this make money?]
**Competitive Advantage**: [What makes this unique?]

## Key Details
**What they're looking for**:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**What they're offering**:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**What makes this interesting**:
- [Interesting aspect 1]
- [Interesting aspect 2]
- [Interesting aspect 3]

## Market Analysis
**Market Size**: [TAM/SAM/SOM]
**Growth Rate**: [Market growth rate]
**Competition**: [Key competitors]
**Barriers to Entry**: [What prevents others from entering?]
**Regulatory Environment**: [Any regulatory considerations?]

## Financial Projections
**Revenue Model**: [How revenue is generated]
**Projected Revenue**: [Year 1, 2, 3 projections]
**Cost Structure**: [Key cost components]
**Break-even**: [When will it break even?]
**Exit Strategy**: [How will investors/partners exit?]

## Decision Timeline
**Decision Deadline**: {deadline or "[Date]"}
**Key Milestones**:
- [ ] Initial conversation: [Date]
- [ ] Due diligence: [Date]
- [ ] Business plan review: [Date]
- [ ] Final decision: [Date]

## Contact Information
**Primary Contact**: [Name, Title, Email, Phone]
**Secondary Contact**: [Name, Title, Email, Phone]
**Relationship**: [How you know them]
**Decision Makers**: [Who makes the final decision?]

## Documents & Resources
- [ ] Business plan
- [ ] Financial projections
- [ ] Market research
- [ ] Legal documents
- [ ] Technical specifications
- [ ] Your proposal/application

## Your Offer/Proposal
**What you're proposing**:
- [Proposal point 1]
- [Proposal point 2]
- [Proposal point 3]

**Your terms**:
- [Investment amount/equity percentage]
- [Role and responsibilities]
- [Timeline/availability]
- [Other requirements]

## Next Steps
- [ ] Action 1 (Owner: [Name], Due: [Date])
- [ ] Action 2 (Owner: [Name], Due: [Date])
- [ ] Action 3 (Owner: [Name], Due: [Date])

---
*Created by Business Opportunity Manager on {datetime.now().strftime("%Y-%m-%d %H:%M")}*
"""
    
    def _create_evaluation_template(self) -> str:
        """Create evaluation template content."""
        return """# Business Opportunity Evaluation

## Evaluation Scores

### Business Potential (35% weight)
- **Market Size** (1-10): ___ - [Total addressable market]
- **Competitive Advantage** (1-10): ___ - [Unique value proposition]
- **Scalability** (1-10): ___ - [Growth potential]
- **Revenue Model** (1-10): ___ - [Path to profitability]

**Business Score**: ___/35

### Goals Alignment (25% weight)
- **Career Growth** (1-10): ___ - [How this advances your entrepreneurial journey]
- **Financial Impact** (1-10): ___ - [Potential financial returns]
- **Learning Opportunity** (1-10): ___ - [New skills/knowledge gained]
- **Network Expansion** (1-10): ___ - [Professional network growth]

**Goals Score**: ___/25

### Values Alignment (25% weight)
- **Fairness** (1-10): ___ - [Fair terms and transparent relationships]
- **Freedom** (1-10): ___ - [Maintains your autonomy]
- **Sustainability** (1-10): ___ - [Long-term sustainability alignment]

**Values Score**: ___/25

### Timing & Execution (15% weight)
- **Current Capacity** (1-10): ___ - [Time/energy availability]
- **Market Timing** (1-10): ___ - [Right time for this opportunity]
- **Execution Risk** (1-10): ___ - [Feasibility of implementation]
- **Life Stage Fit** (1-10): ___ - [Fits current life priorities]

**Timing Score**: ___/15

**Total Score**: ___/100

## Decision Framework Analysis

### 10/10/10 Rule
- **10 minutes**: [How you'll feel immediately]
- **10 months**: [How you'll feel in 10 months]
- **10 years**: [How you'll feel in 10 years]

### Reversibility Assessment
- **Decision Type**: One-way door | Two-way door
- **Reversibility**: Easy | Moderate | Difficult | Impossible
- **Exit Strategy**: [How you could exit if needed]

### Risk Assessment
- **Market Risk**: Low | Medium | High
- **Execution Risk**: Low | Medium | High
- **Financial Risk**: Low | Medium | High
- **Reputation Risk**: Low | Medium | High
- **Mitigation Strategies**: [How to reduce risks]

## Pros & Cons

### Pros
- [Pro 1]
- [Pro 2]
- [Pro 3]

### Cons
- [Con 1]
- [Con 2]
- [Con 3]

## Questions to Ask
- [ ] What is the total addressable market?
- [ ] Who are the main competitors?
- [ ] What is the competitive advantage?
- [ ] How will the business make money?
- [ ] What are the key risks?
- [ ] Who is on the team?
- [ ] What is the funding status?
- [ ] What is the exit strategy?

## Decision Log
**Date**: [Date]
**Decision**: [Accept/Decline/On Hold]
**Rationale**: [Why you made this decision]
**Key Factors**: [Most important factors in decision]

## Follow-up Actions
- [ ] Follow-up action 1
- [ ] Follow-up action 2
- [ ] Follow-up action 3

## Lessons Learned
*To be filled after decision and experience*

---
*Evaluation template created by Business Opportunity Manager*
"""
    
    def _create_timeline_template(self, deadline: str) -> str:
        """Create timeline template content."""
        return f"""# Business Opportunity Timeline

## Key Dates
**Decision Deadline**: {deadline or "[Date]"}
**Created**: {datetime.now().strftime("%Y-%m-%d")}

## Milestones
- [ ] **Initial Contact**: [Date] - [Description]
- [ ] **Information Gathering**: [Date] - [Description]
- [ ] **Business Analysis**: [Date] - [Description]
- [ ] **Due Diligence**: [Date] - [Description]
- [ ] **Decision**: [Date] - [Description]
- [ ] **Implementation**: [Date] - [Description]

## Important Notes
- [Note 1]
- [Note 2]
- [Note 3]

## Reminders
- [ ] Set reminder for decision deadline
- [ ] Follow up on pending actions
- [ ] Update stakeholders on progress

---
*Timeline created by Business Opportunity Manager*
"""
    
    def _update_evaluation_file(self, opportunity_path: Path, scores: Dict[str, int], total_score: int):
        """Update evaluation file with scores."""
        evaluation_path = opportunity_path / "evaluation.md"
        
        # Read current content
        with open(evaluation_path, "r") as f:
            content = f.read()
        
        # Update scores
        content = content.replace("**Market Size** (1-10): ___", f"**Market Size** (1-10): {scores.get('market_size', 0)}")
        content = content.replace("**Competitive Advantage** (1-10): ___", f"**Competitive Advantage** (1-10): {scores.get('competitive_advantage', 0)}")
        content = content.replace("**Scalability** (1-10): ___", f"**Scalability** (1-10): {scores.get('scalability', 0)}")
        content = content.replace("**Revenue Model** (1-10): ___", f"**Revenue Model** (1-10): {scores.get('revenue_model', 0)}")
        content = content.replace("**Business Score**: ___/35", f"**Business Score**: {sum([scores.get(k, 0) for k in ['market_size', 'competitive_advantage', 'scalability', 'revenue_model']])}/35")
        
        content = content.replace("**Career Growth** (1-10): ___", f"**Career Growth** (1-10): {scores.get('career_growth', 0)}")
        content = content.replace("**Financial Impact** (1-10): ___", f"**Financial Impact** (1-10): {scores.get('financial_impact', 0)}")
        content = content.replace("**Learning Opportunity** (1-10): ___", f"**Learning Opportunity** (1-10): {scores.get('learning_opportunity', 0)}")
        content = content.replace("**Network Expansion** (1-10): ___", f"**Network Expansion** (1-10): {scores.get('network_expansion', 0)}")
        content = content.replace("**Goals Score**: ___/25", f"**Goals Score**: {sum([scores.get(k, 0) for k in ['career_growth', 'financial_impact', 'learning_opportunity', 'network_expansion']])}/25")
        
        content = content.replace("**Fairness** (1-10): ___", f"**Fairness** (1-10): {scores.get('fairness', 0)}")
        content = content.replace("**Freedom** (1-10): ___", f"**Freedom** (1-10): {scores.get('freedom', 0)}")
        content = content.replace("**Sustainability** (1-10): ___", f"**Sustainability** (1-10): {scores.get('sustainability', 0)}")
        content = content.replace("**Values Score**: ___/25", f"**Values Score**: {sum([scores.get(k, 0) for k in ['fairness', 'freedom', 'sustainability']])}/25")
        
        content = content.replace("**Current Capacity** (1-10): ___", f"**Current Capacity** (1-10): {scores.get('current_capacity', 0)}")
        content = content.replace("**Market Timing** (1-10): ___", f"**Market Timing** (1-10): {scores.get('market_timing', 0)}")
        content = content.replace("**Execution Risk** (1-10): ___", f"**Execution Risk** (1-10): {scores.get('execution_risk', 0)}")
        content = content.replace("**Life Stage Fit** (1-10): ___", f"**Life Stage Fit** (1-10): {scores.get('life_stage_fit', 0)}")
        content = content.replace("**Timing Score**: ___/15", f"**Timing Score**: {sum([scores.get(k, 0) for k in ['current_capacity', 'market_timing', 'execution_risk', 'life_stage_fit']])}/15")
        
        content = content.replace("**Total Score**: ___/100", f"**Total Score**: {total_score}/100")
        
        # Add evaluation summary
        evaluation_summary = f"""

## Evaluation Summary
**Evaluation Date**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Total Score**: {total_score}/100
**Recommendation**: {self._get_recommendation(total_score)}

### Score Breakdown
- Business Potential: {sum([scores.get(k, 0) for k in ['market_size', 'competitive_advantage', 'scalability', 'revenue_model']])}/35
- Goals Alignment: {sum([scores.get(k, 0) for k in ['career_growth', 'financial_impact', 'learning_opportunity', 'network_expansion']])}/25
- Values Alignment: {sum([scores.get(k, 0) for k in ['fairness', 'freedom', 'sustainability']])}/25
- Timing & Execution: {sum([scores.get(k, 0) for k in ['current_capacity', 'market_timing', 'execution_risk', 'life_stage_fit']])}/15

"""
        
        content += evaluation_summary
        
        # Write updated content
        with open(evaluation_path, "w") as f:
            f.write(content)
    
    def _get_recommendation(self, score: int) -> str:
        """Get recommendation based on score."""
        if score >= 90:
            return "Exceptional opportunity - Strong yes"
        elif score >= 80:
            return "Very good opportunity - Likely yes"
        elif score >= 70:
            return "Good opportunity - Consider carefully"
        elif score >= 60:
            return "Moderate opportunity - Proceed with caution"
        elif score >= 50:
            return "Poor opportunity - Likely no"
        else:
            return "Very poor opportunity - Strong no"

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Business Opportunity Management System")
    parser.add_argument("--base-path", help="Base path for business opportunities")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create opportunity command
    create_parser = subparsers.add_parser("create", help="Create a new business opportunity")
    create_parser.add_argument("name", help="Business opportunity name")
    create_parser.add_argument("type", help="Business opportunity type")
    create_parser.add_argument("source", help="How you learned about this opportunity")
    create_parser.add_argument("--deadline", help="Decision deadline (YYYY-MM-DD)")
    create_parser.add_argument("--priority", choices=["High", "Medium", "Low"], default="Medium")
    
    # Evaluate opportunity command
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate a business opportunity")
    eval_parser.add_argument("opportunity_id", help="Business opportunity ID")
    eval_parser.add_argument("--scores", help="JSON string with scores")
    
    # List opportunities command
    list_parser = subparsers.add_parser("list", help="List all business opportunities")
    
    # Check deadlines command
    deadlines_parser = subparsers.add_parser("deadlines", help="Check upcoming deadlines")
    
    # Archive opportunity command
    archive_parser = subparsers.add_parser("archive", help="Archive a business opportunity")
    archive_parser.add_argument("opportunity_id", help="Business opportunity ID")
    archive_parser.add_argument("status", help="Final status")
    archive_parser.add_argument("--notes", help="Archive notes")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = BusinessOpportunityManager(args.base_path)
    
    if args.command == "create":
        opportunity_id = manager.create_opportunity(
            args.name, args.type, args.source, args.deadline, args.priority
        )
        print(f"Created business opportunity: {opportunity_id}")
    
    elif args.command == "evaluate":
        if args.scores:
            scores = json.loads(args.scores)
            result = manager.evaluate_opportunity(args.opportunity_id, scores)
            print(f"Evaluation complete: {result}")
        else:
            print("Please provide scores using --scores argument")
    
    elif args.command == "list":
        opportunities = manager.get_opportunities_summary()
        print(f"Active Business Opportunities ({len(opportunities)}):")
        for opp in opportunities:
            print(f"  {opp['id']}: {opp['name']} ({opp['type']}) - Score: {opp.get('score', 'Not evaluated')}")
    
    elif args.command == "deadlines":
        deadlines = manager.check_deadlines()
        if deadlines:
            print("Upcoming Deadlines:")
            for opp in deadlines:
                print(f"  {opp['name']}: {opp['days_until_deadline']} days ({opp['deadline']})")
        else:
            print("No upcoming deadlines")
    
    elif args.command == "archive":
        manager.archive_opportunity(args.opportunity_id, args.status, args.notes or "")

if __name__ == "__main__":
    main()

