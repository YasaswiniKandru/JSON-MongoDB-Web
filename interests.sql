
DROP TABLE if EXISTS main_table;
DROP TABLE if EXISTS checkbox;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE main_table (
sno INT,
firstname VARCHAR(100),
lastname VARCHAR(100),
status VARCHAR(100),
semester VARCHAR(100),
primary key (sno)
);


CREATE TABLE checkbox (
courses VARCHAR(100),
sno INT,
primary key (sno,courses),
foreign key (sno) references main_table(sno)
);