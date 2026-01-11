INSERT OR IGNORE INTO version_testing(test)
VALUES(1);

UPDATE version_testing
SET
    num_applied = num_applied + 1
WHERE test == 1;
