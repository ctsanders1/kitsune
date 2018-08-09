# NEXT STEPS

1. Test each of the badges below, ensuring they are all triggered/awarded correctly.
    a. I already decreased the thresholds in `.env.`
2. Get tests passing


# Current badges

All badges are auto-created/renewed for each year. For example, in 2018, the following badges exist:

- 2018-support-forum-badge
- 2018-army-of-awesome-badge
- 2018-kb-badge
- 2018-l10n-badge

## Army of awesome badge

Awarded when a `kitsune.customercare.Reply` model is saved if it's the user's 50th reply.

These are actually tweets from the Twitter. Very cumbersome to test manually.

### Code trail

1. `on_reply_save` in `kitsune/customercare/badges.py`
2. `maybe_award_badge` in `kitsune/customercare/tasks.py`

## STR

1. Just run the tests.

## Support forum badge

Awarded when a `kitsune.questions.Answer` model is saved if it's the user's 30th answer.

### Code trail

1. `on_reply_save` in `kitsune/questions/badges.py`
2. `maybe_award_badge` in `kitsune/questions/tasks.py`

## STR

1.

## KB and L10n badges

Awarded when a `kitsune.wiki.Revision` model is saved.

If it's the user's 10th revision in the default locale (en-US), the **KB badge** is awarded.

If it's the user's 10th revision *not* in the default locale (en-US), the **L10n badge** is awarded.

### Code trail

1. `on_revision_save` in `kitsune/wiki/badges.py`
2. `maybe_award_badge` in `kitsune/wiki/tasks.py`

## Badge auto-creation

All badges above eventually call `get_or_create_badge` in `kitsune/kbadge/utils.py`. This function does what it says on the tin - retrieves or creates the requested badge for the given year.
