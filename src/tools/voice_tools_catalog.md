# Vita Voice Agent — Tool Catalog (49 Tools)

> These tools are registered with Google ADK and available during Gemini 3.1 Flash Live voice sessions.

---

## User Context & Retrieval

| Tool | Purpose | Returns |
|------|---------|---------|
| `get_user_context()` | Full elder profile, meds, appointments, memories | Complete context object |
| `read_medications()` | List all active medications | Medication list + display card |
| `read_appointments()` | Upcoming appointments | Appointment list + display card |
| `read_who_am_i()` | Elder's profile summary + family + key memories | Identity card |
| `get_today_tasks()` | Today's meds, appointments, check-in status | Daily checklist |
| `get_current_time()` | Current time/date in elder's timezone | Datetime string |

## Health & Safety

| Tool | Purpose | Side Effects |
|------|---------|-------------|
| `log_mood(score)` | Record 1-5 mood score | Saves to session, visible on caregiver dashboard |
| `log_pain(score, location)` | Record pain score + body area | Saves to session |
| `confirm_medication_taken(med_id)` | Log medication adherence | Updates adherence chart for caregivers |
| `flag_for_caregiver(tier, description)` | Silent alert (1=urgent, 2=today, 3=weekly) | Pushes notification to all caregivers |
| `fall_risk_assessment()` | Voice-driven fall risk check | Auto-flags caregiver if medium/high risk |
| `medication_interaction_check(new_med)` | Check new med vs current meds | Non-diagnostic, flags caregiver |
| `doctor_visit_debrief()` | Record what doctor said (elder's words) | Saves to caregiver dashboard |

## Food & Nutrition

| Tool | Purpose |
|------|---------|
| `order_food()` | Place order from favorites list (caregiver approval) |
| `search_recipe(query)` | Search + generate full recipe with ingredients/steps |
| `save_recipe()` | Save to personal cookbook |
| `add_grocery_item(item)` | Add to shared grocery list |

## Family Connection

| Tool | Purpose |
|------|---------|
| `call_family(name)` | Look up family member → phone/WhatsApp/FaceTime link |
| `family_tree_builder(person, relationship, story)` | Record family relationships and stories |
| `photo_share()` | Elder takes photo → Vita captions → sends to family |
| `virtual_window(family_member)` | Describe what family member's day looks like right now |

## Libro de Vida & Wellbeing

| Tool | Purpose |
|------|---------|
| `record_life_story(story, era, topic)` | Save elder's personal stories with tags |
| `save_memory(fact, category)` | Save facts/memories from conversation |
| `teach_me_something()` | Elder teaches Vita a recipe/song/craft (reverses power) |
| `gratitude_journal()` | Daily 1-3 good things (proven depression intervention) |
| `worry_jar(worry)` | Save anxieties (private, therapeutic) |

## Daily Wellness

| Tool | Purpose |
|------|---------|
| `sleep_journal(quality, hours)` | Log sleep (flags 3+ bad nights to caregiver) |
| `hydration_tracker(glasses)` | Track water intake (dehydration = #1 preventable hosp.) |
| `visitor_log(who)` | Log who visited (makes loneliness visible) |
| `bill_reminder(bill, due_date)` | Track bill payments |
| `schedule_reminder(task, day, time)` | Create weekly reminder |

## Enrichment & Entertainment

| Tool | Purpose |
|------|---------|
| `search_and_display(query)` | Search movies/music/recipes → display with image/YouTube |
| `read_aloud(type)` | Generate + read: news, Bible, poems, jokes, stories |
| `display_visual_media(url, caption)` | Show image/video overlay during voice session |
| `hide_visual_card()` | Clean up visual overlay |

## Atmosphere & Navigation

| Tool | Purpose |
|------|---------|
| `set_ui_atmosphere(theme)` | Change app background (calm/nature/energize/nostalgia) |
| `trigger_meditation_mode()` | Activate breathing visual overlay |
| `navigate_to(page)` | Request frontend navigation |
| `display_card(title, body, image)` | Show info card during voice |

## Onboarding (Caregiver Setup Mode)

| Tool | Purpose |
|------|---------|
| `save_elder_profile(name, dob, timezone)` | Save basic elder info |
| `save_elder_family_member(name, relationship, phone)` | Save family contact |
| `save_elder_medication(name, dosage, schedule)` | Save medication |
| `save_elder_interests(interests)` | Save hobbies/interests |
| `save_elder_favorite_food(meal)` | Save favorite meal |
