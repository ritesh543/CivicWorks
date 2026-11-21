# Contract specifications

All ten contracts expose `count()` as a view. Indexed records start at 0. Views that return a record return a JSON string. Integers named `*_minute` represent the caller's Unix minutes in UTC. Returned result codes are part of the interface.

## AccessPath

| Method | Effect |
| --- | --- |
| `assess(venue, route, public_evidence)` | Returns a card index. Records the signer, route and evidence fingerprint. |
| `get_report(index)` | Reads the three feature results and the evidence fingerprint. |

The three labels correspond to step-free entry, an accessible restroom reachable from that route, and a lift that serves the route. Each can be `YES`, `NO`, `UNKNOWN` or `CONFLICT`. Validators must reproduce the entire ordered vector. The signed card represents an evaluation of the quoted evidence for the specified route.

## WorksConflict

| Method | Effect |
| --- | --- |
| `compare(first_location, first_start, first_end, first_full, second_location, second_start, second_end, second_full)` | Records overlapping minutes and an outcome. Each `full` flag indicates a full closure. |
| `get_check(index)` | Reads the input windows, location relation and outcome. |

Windows include their start and exclude their end. When two windows overlap, validators classify whether they affect the same access corridor. Results include `NO_TIME_OVERLAP`, `SEPARATE_SEGMENTS`, `REVIEW_LOCATION`, `COORDINATE` and `FULL_CONFLICT`. The last result requires two full closures and the same corridor.

## RepairMerge

| Method | Effect |
| --- | --- |
| `file_report(site_code, observed_minute, observation)` | Opens a new ticket and returns its index. |
| `review_duplicate(newer_index, primary_index)` | Records `SAME_FAULT`, `DIFFERENT` or `UNCLEAR`. Only `SAME_FAULT` creates a link. |
| `get_report(index)`, `get_review(index)`, `review_count()` | Reads observations, duplicate links and review history. |

Both tickets must belong to the signer, share a site code, and have observations within 24 hours. The target must have an earlier index and both tickets must be unlinked. A ticket that already serves as a primary cannot itself become a duplicate. This keeps links at one level.

## NoticeClock

| Method | Effect |
| --- | --- |
| `NoticeClock(minimum_lead_minutes)` | Sets the immutable minimum posting lead time. The published instance uses 1,440 minutes. |
| `check(scope, effective_label, posted_minute, effective_minute, notice)` | Records whether the notice identifies the service and location, change, and effective time, plus the calculated posting lead time. |
| `minimum_lead()`, `get_report(index)` | Reads the threshold or the evaluated notice. |

A notice passes when the content is `COMPLETE` and the caller's effective minute minus posted minute meets the threshold. The result preserves that calculation, the separate content verdict, and a digest of the quoted notice.

## OpenFieldMap

| Method | Effect |
| --- | --- |
| `propose(feed_revision, source_column, description, source_unit, target)` | Reviews equivalence of the public column definition to the target. |
| `activate(index)` | The publisher commits a `MATCH` proposal for an unmapped column in that feed revision. |
| `active_proposal(publisher, feed_revision, source_column)` | Returns the active index or `-1`. |
| `normalize(index, source_value)`, `get_proposal(index)` | Applies the active integer multiplier or reads the proposal. |

| Target | Input units | Output unit |
| --- | --- | --- |
| `PATH_WIDTH`, `DOOR_CLEARANCE` | `mm`, `cm`, `m` | `mm` |
| `CLOSURE_DURATION` | `s`, `min`, `h` | `s` |
| `TANK_CAPACITY` | `ml`, `l` | `ml` |

A publisher can use a new feed revision to introduce a new mapping. The chosen source unit fixes the multiplier, and the submitted column description provides the evidence for the semantic match.

## HandoffCondition

| Method | Effect |
| --- | --- |
| `offer(asset_ref, recipient, expected_condition)` | Opens an inspection for a named wallet and prevents overlapping offers for that sender and asset. |
| `inspect(index, observed_condition)` | The recipient enters an inspection. `MATCH` accepts it. `CHANGED` and `UNCLEAR` open a review for the sender. |
| `resolve_exception(index, accept, public_reason)` | The sender accepts or declines a recorded exception. |
| `cancel_offer(index)`, `get_handoff(index)` | The sender can cancel an uninspected offer. Anyone can view the record. |

The two signers create an auditable condition record. Physical custody follows the parties' workflow.

## DonationAllocation

| Method | Effect |
| --- | --- |
| `open_channel(name, acceptance_rule, capacity)` | Creates an organizer-owned channel with whole-unit capacity. |
| `submit_lot(channel_index, lot_ref, quantity, description)` | Records the semantic eligibility of one lot for that channel. |
| `reserve(lot_index)` | Moves capacity from remaining to reserved for an eligible lot. |
| `complete(lot_index, distributed)` | Completes distribution or releases the reservation. |
| `lot_count()`, `get_channel(index)`, `get_lot(index)` | Reads capacity and lot status. |

Only the organizer can reserve or complete a lot. Remaining, reserved and distributed units always sum to original capacity. A completed or released lot cannot be reserved again.

## MinutesCommitment

| Method | Effect |
| --- | --- |
| `publish(meeting_ref, public_minutes)` | Stores up to 40 nonempty lines and a fingerprint of the public record. |
| `certify(meeting_index, action, assignee, deadline)` | The publisher asks validators to verify a specific commitment. Repeating the same claim returns the original index. |
| `certification_count()`, `get_minutes(index)`, `get_certification(index)` | Reads minutes and the claim, result and exact selected line. |

The leader proposes a numbered line or reports absence. For a positive result, the validator checks the selected line against the exact action, assignee and deadline, plus the full minutes for a later reversal. For absence, the validator independently searches for an approval.

## MeterContinuity

| Method | Effect |
| --- | --- |
| `register(asset_ref, dial_modulus, maximum_increment, initial, observed_minute)` | Registers an operator's meter and baseline. The display range is zero up to the modulus, exclusive. |
| `observe(meter_index, display, observed_minute, service_note)` | Records a normal reading, a confirmed wrap, a confirmed replacement after a backward reading, or a held result. |
| `reading_count()`, `get_meter(index)`, `get_reading(index)` | Reads the current baseline, cumulative credited units and reading history. |

A suspected wrap uses `dial_modulus - previous + display` and must fit the configured maximum increment. A replacement after a backward reading starts a new segment. A held reading adds an audit record and leaves the accepted baseline available for a corrected submission.

## PublicFeedPulse

| Method | Effect |
| --- | --- |
| `open_watch(subject, first_url, second_url)` | Pins two approved HTTPS sources on distinct hosts and a resource or service label. |
| `refresh(watch_index, next_round)` | The publisher asks validators to fetch both sources and classify each excerpt. |
| `scan_count()`, `get_watch(index)`, `get_scan(index)` | Reads the latest confirmation state and each source snapshot's labels. |

Validators agree on the ordered pair of `LISTED`, `PAUSED`, `UNKNOWN` or `UNREACHABLE`. Two consecutive observations with the same pair of matching positive labels establish `LISTED` or `PAUSED`. A mismatched or missing observation returns the watch to `UNCONFIRMED`. Rounds are transaction sequence numbers controlled by the watch publisher. Consumers who need time separation should schedule calls accordingly.
