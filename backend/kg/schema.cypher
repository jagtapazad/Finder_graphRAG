// Unique constraints
CREATE CONSTRAINT agent_name_unique IF NOT EXISTS
FOR (a:Agent)
REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT capability_name_unique IF NOT EXISTS
FOR (c:Capability)
REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT tasktype_name_unique IF NOT EXISTS
FOR (t:TaskType)
REQUIRE t.name IS UNIQUE;

// Indexes for faster lookup
CREATE INDEX query_text_index IF NOT EXISTS
FOR (q:Query)
ON (q.text);

CREATE INDEX routing_timestamp_index IF NOT EXISTS
FOR (rd:RoutingDecision)
ON (rd.timestamp);


