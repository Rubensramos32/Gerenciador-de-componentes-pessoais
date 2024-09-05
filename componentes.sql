BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "componentes" (
	"codigo_componente"	TEXT,
	PRIMARY KEY("codigo_componente")
);
INSERT INTO "componentes" VALUES ('215.0000.01');
INSERT INTO "componentes" VALUES ('297.1416.00');
INSERT INTO "componentes" VALUES ('295.1422.00');
INSERT INTO "componentes" VALUES ('255.1522.00');
INSERT INTO "componentes" VALUES ('298.1420.00');
INSERT INTO "componentes" VALUES ('240.0105.00');
INSERT INTO "componentes" VALUES ('241.0104.50');
INSERT INTO "componentes" VALUES ('210.0000.00');
INSERT INTO "componentes" VALUES ('210.0101.00');
INSERT INTO "componentes" VALUES ('373.0450.00');
COMMIT;
