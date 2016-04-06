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
    ('<unknown>', "Please restate your question in the form of a bucket."),
    ('<unknown>', "Please restate your question in the form of a giraffe."),
    ('<get item>', "Thanks, I'll take %received."),
    ('<get item>', "Sure, I'll take %received."),
    ('<get item>', "Okay, $who."),
    ('<replace item>', "_drops $item and takes %received._"),
    ('<replace item>', "_hands $who $item and takes %received._"),
    ('<duplicate item>', "I already have one of those."),
    ('<inventory empty>', "But I'm empty : ("),
    ('<drop item>', "_gives $who $item_"),
    ('<drop item>', "_hands $who $item_"),
    ('<drop item>', "_drops $item_"),
    ('<vague quote>', "You're going to have to be a little more specific than that, $who."),
    ('<vague quote>', "That doesn't give me a lot to work with."),
    ('<no quote>', "Y'all haven't old me to remember anything about this guy."),
    ('<no quote>', "Lemme think.... .. .... .. Nope. I got nothin'."),
    ('<no quote>', "I don't remember anything.");
