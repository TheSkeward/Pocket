--- Sample starter facts and tidbits and/or testing facts for Pocket

INSERT OR IGNORE INTO comments (triggers, remark, protected) VALUES
    ('...', '[A bird chirps in the distance]', 1),
    ('...', '[$someone drops their phone]', 1),
    ('exactly', 'I said it better earlier.', 1);

INSERT OR IGNORE INTO auto_responses (command, response) VALUES
    ('<unknown>', "I don't know anything about that, $who."),
    ('<unknown>', "BEEEEEEP BOOP BOOOOOP WHEEEEEeeee"),
    ('<unknown>', "How should I know? I'm just a bot."),
    ('<get item>', "Thanks, I'll take %received."),
    ('<get item>', "Ok, $who."),
    ('<replace item>', "/me drops $item and takes %received."),
    ('<replace item>', "/me hands $who $item and takes %received."),
    ('<duplicate item>', "I already have one of those."),
    ('<inventory empty>', "But I'm empty : ("),
    ('<drop item>', "/me gives $who $item");
