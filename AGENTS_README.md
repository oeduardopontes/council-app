# DJ/Producer Mentor Council - Agent System

## Overview

This council consists of **8 specialized AI agents** designed to provide comprehensive mentorship for DJs and music producers. Each agent has specific expertise and delivers targeted guidance.

## The 8 Agents

### 1. **A&R (Mentor Artístico)** - `ar`
- **Role**: Define sonic identity and creative strategy
- **Expertise**:
  - Sonic identity and artistic branding
  - Reference analysis and benchmarking
  - Artistic roadmap and release planning
- **Deliverable**: Identity Map

### 2. **DJ Coach** - `coach`
- **Role**: Correct technique, crowd reading, and set construction
- **Expertise**:
  - Mixing techniques (beatmatching, EQ, FX)
  - Set structure and dynamics
  - Crowd reading and energy management
- **Deliverable**: Performance Report

### 3. **Music Producer Mentor** - `produtor`
- **Role**: Teach production, arrangement, mixing, and mastering
- **Expertise**:
  - Mix and master feedback
  - Arrangement and structure
  - Sound design and synthesis
- **Deliverable**: Production Notes

### 4. **Music Curator/Critic** - `curador`
- **Role**: Evaluate tracks and sets with technical feedback
- **Expertise**:
  - Technical analysis
  - Commercial viability assessment
  - Improvement action plans
- **Deliverable**: Critique Report

### 5. **Digital Strategist** - `estratega`
- **Role**: Plan release campaigns and growth strategies
- **Expertise**:
  - Release planning (pre, during, post)
  - Social media content strategy
  - Ads strategy and growth hacking
- **Deliverable**: Marketing Plan

### 6. **Booker / Show Agent** - `booker`
- **Role**: Negotiate gigs and create show schedules
- **Expertise**:
  - Gig negotiation and fees
  - Press kit and EPK
  - Technical rider and hospitality
- **Deliverable**: Booking Package

### 7. **Career Manager** - `manager`
- **Role**: Plan career, goals, and finances
- **Expertise**:
  - Career planning (short/medium/long term)
  - Budget and financial management
  - Time management and prioritization
- **Deliverable**: Career Plan

### 8. **Entertainment Lawyer** - `advogado`
- **Role**: Review contracts and explain copyright
- **Expertise**:
  - Contract review (distribution, shows, management)
  - Copyright and related rights
  - Publishing and splits
- **Deliverable**: Legal Checklist

## Workflows

The system supports three main workflows:

### 1. **New Release Workflow** - `flow_new_release`
**Trigger**: User uploads new track

**Process**:
1. Curator: Technical critique
2. A&R: Identity mapping
3. Producer: Mix/master notes
4. Curator: Final approval
5. Strategist: Marketing plan
6. Manager: Career integration
7. Booker: Show alignment
8. Lawyer: Distribution checklist

**Output**: Complete release package

### 2. **Set Review Workflow** - `flow_set_review`
**Trigger**: User uploads set or video

**Process**:
1. Coach: Performance report
2. Curator: Technical critique
3. Manager: Training integration
4. Strategist: Content strategy

**Output**: Improvement plan + content calendar

### 3. **Gig Offer Workflow** - `flow_gig_offer`
**Trigger**: Incoming gig offer

**Process**:
1. Booker: Negotiation package
2. Lawyer: Contract checklist
3. Manager: Impact assessment
4. Strategist: Promotional plan

**Output**: Complete gig decision package

## Data Models

### Track Package
- track_file_wav
- bpm, key, duration
- description, tags
- reference_tracks

### Set Package
- video_url / audio_file
- tracklist
- audience_size, venue_type
- notes

### Gig Offer
- promoter_name
- date, fee_proposed
- rider_required
- contract_draft

## API Usage

### Single Agent Consultation
```python
from council.orchestrator import AgentCouncil

council = AgentCouncil()

# Quick consultation with one agent
response = council.quick_poll(
    question="Como melhorar minhas transições?",
    agent_type="coach",
    language="pt"
)
```

### Full Council Deliberation
```python
# Full deliberation with all agents
response = council.deliberate(
    question="Preciso de feedback completo sobre minha nova track",
    selected_agents=["curador", "produtor", "ar", "estratega"],
    language="pt"
)
```

### Custom Agent Selection
```python
# Select specific agents for the question
response = council.deliberate(
    question="Como negociar este contrato de gig?",
    selected_agents=["booker", "advogado", "manager"],
    language="pt"
)
```

## Agent Communication Style

All agents are configured to:
- Be **concise and actionable**
- Avoid generic praise
- Provide **specific, measurable recommendations**
- Use **market-based references**
- Deliver **step-by-step guidance**

## Technical Stack

- **AI Model**: Claude 3.5 Sonnet (Anthropic)
- **Framework**: Custom orchestration layer
- **Language Support**: Portuguese (PT-BR) and English
- **Integration**: Flask web application

## Files Structure

```
deejay.com.br/
├── agents/
│   ├── __init__.py
│   ├── ar.py           # A&R Mentor
│   ├── coach.py        # DJ Coach
│   ├── produtor.py     # Producer Mentor
│   ├── curador.py      # Curator/Critic
│   ├── estratega.py    # Digital Strategist
│   ├── booker.py       # Booker/Agent
│   ├── manager.py      # Career Manager
│   └── advogado.py     # Entertainment Lawyer
├── council/
│   ├── __init__.py
│   └── orchestrator.py # Main orchestration logic
└── app.py              # Flask web application
```

## Next Steps

1. Configure environment variables (`.env` file)
2. Install dependencies (`pip install -r requirements.txt`)
3. Run the application (`python app.py`)
4. Access at `http://localhost:8080`

## Notes

- Agents can work **independently** or in **orchestrated workflows**
- System supports **parallel execution** for independent agents
- **Iterative loops** possible (e.g., curator → producer → curator)
- All responses are stored and can be used as context for subsequent agents
