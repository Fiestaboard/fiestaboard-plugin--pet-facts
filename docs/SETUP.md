# Pet Facts Setup Guide

Display a random fun fact about cats or dogs.

## Overview

The Pet Facts plugin fetches a random cat or dog fact from free public APIs. Cat facts come from catfact.ninja; dog facts from dogapi.dog. Configure the animal type or let it randomize each refresh. No API key required.

- API reference: https://catfact.ninja/

### Prerequisites

No API key required.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **Pet Facts**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `pet_facts` plugin variables:
   ```
   {{{ pet_facts.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `pet_facts.fact` | The pet fact | `Cats sleep 12-16 hours` |
| `pet_facts.animal` | The animal type (cat or dog) | `cat` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `animal` | Animal | Which animal facts to show. | `random` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to fetch a new fact. | `300` |

## Troubleshooting

- **API error** — both APIs are free and require no key; check network connectivity.
- **Fact too long** — facts are truncated to 22 characters for the board display.

