--- Sample starter facts and tidbits and/or testing facts for Pocket

INSERT OR IGNORE INTO comments (triggers, remark, protected) VALUES
    ('...', '[A bird chirps in the distance]', 1),
    ('...', '[$someone drops their phone]', 1),
    ('exactly', 'I said it better earlier.', 1);

INSERT OR IGNORE INTO auto_responses (command, response) VALUES
    ('<unknown>', "I don't know anything about that, $who."),
    ('<unknown>', "BEEEEEEP BOOP BOOOOOP WHEEEEEeeee"),
    ('<unknown>', "How should I know? I'm just a bot."),
    ('<unknown>', "Why would you ask me that?"),
    ('<unknown>', "How would I bloody know?"),
    ('<unknown>', "ERROR 432018: COMMAND NOT IN DATABASE. PLEASE CONTACT YOUR LOCAL GALAXY ENGINEER"),
    ('<unknown>', "BEEEEEEEEeeeeeeeEEeeeEEEEEPPP"),
    ('<get item>', "Thanks, I'll take %received."),
    ('<get item>', "Sure, I'll take %received."),
    ('<get item>', "Okay, $who."),
    ('<replace item>', "_drops $item and takes %received._"),
    ('<replace item>', "_hands $who $item and takes %received._"),
    ('<duplicate item>', "I already have one of those."),
    ('<inventory empty>', "But I'm empty : ("),
    ('<drop item>', "_gives $who $item_"),
    ('<drop item>', "_hands $who $item_"),
    ('<drop item>', "_drops $item_");
