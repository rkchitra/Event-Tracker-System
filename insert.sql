SET foreign_key_checks = 0;
drop table if exists events;
drop table if exists login;
drop table if exists notify;
drop table if exists pevents;
drop table if exists reg;
SET foreign_key_checks = 1;


#Table creation
CREATE TABLE events (
  cname varchar(50) DEFAULT NULL,
  ename varchar(100) NOT NULL,
  edescp varchar(400) DEFAULT NULL,
  seats int(4) DEFAULT NULL,
  dt varchar(10) DEFAULT NULL,
  tm varchar(8) DEFAULT NULL,
  venue varchar(40) DEFAULT NULL,
  big_event varchar(3) DEFAULT NULL,
  PRIMARY KEY (ename)
);
CREATE TABLE login (
  name varchar(70) DEFAULT NULL,
  email varchar(50) NOT NULL,
  usn varchar(10) DEFAULT NULL,
  pno varchar(12) DEFAULT NULL,
  passwd varchar(30) DEFAULT NULL,
  eh varchar(1) DEFAULT 'N',
  PRIMARY KEY (email)
);

CREATE TABLE notify (
  email varchar(50) DEFAULT NULL,
  cname varchar(30) DEFAULT NULL,
  FOREIGN KEY (email) REFERENCES login (email) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE pevents (
  cname varchar(50) DEFAULT NULL,
  ename varchar(100) DEFAULT NULL,
  edescp varchar(400) DEFAULT NULL,
  dt varchar(10) DEFAULT NULL,
  big_event varchar(3) DEFAULT NULL
);
 CREATE TABLE reg (
  ename varchar(100) DEFAULT NULL,
  sname varchar(50) DEFAULT NULL,
  usn varchar(10) DEFAULT NULL,
  email varchar(50) DEFAULT NULL,
  ph varchar(10) DEFAULT NULL,
  memb varchar(3) DEFAULT NULL,
  FOREIGN KEY (email) REFERENCES login (email) ON UPDATE CASCADE ON DELETE CASCADE
);


drop trigger if exists update_seat_count;
drop procedure if exists unregister;
drop procedure if exists update_events;
drop view if exists details;
drop function if exists event_num;
drop index if exists em;

#Trigger
delimiter //
CREATE TRIGGER update_seat_count
AFTER INSERT ON reg FOR EACH ROW
BEGIN
update events SET seats = seats-1 where ename = NEW.ename;
END //
delimiter ;

 #Procedures 
delimiter //
CREATE PROCEDURE unregister(eve_name varchar(50),em varchar(50))
BEGIN
delete from reg where email=em and ename=eve_name;
update events set seats=seats+1 where ename=eve_name;
END;
//
delimiter ;

delimiter //
 CREATE PROCEDURE update_events()
BEGIN
insert into pevents (SELECT cname,ename,edescp,dt,big_event from events where events.dt<curdate());
delete from events where events.dt<curdate();
END
//
delimiter ;

#VIEWS
CREATE VIEW details AS SELECT name,email,usn,pno,eh from login;

#INDEX
CREATE INDEX em login(email);

#FUNCTION
delimiter $$
CREATE FUNCTION event_num(em varchar(50)) RETURNS int
BEGIN
declare num int
SELECT count(*) into num from reg where email=em and ename in (select ename from event);
return num;
END $$
delimiter ;

#INSERT STATEMENTS FOR EVENT HANDLERS 
insert into login(name,email,usn,passwd,eh) values('Force Ikshvaku','force_ikshvaku@gmail.com','N/A','forcee','Y');
insert into login(name,email,usn,passwd,eh) values('IEEE','ieee@gmail.com','N/A','IEEEE','Y');
insert into login(name,email,usn,passwd,eh) values('ISSA','issa@gmail.com','N/A','ISSAA','Y');
insert into login(name,email,usn,passwd,eh) values('NIE','nie@gmail.com','N/A','NIEE','Y');
insert into login(name,email,usn,passwd,eh) values('Onyx','Onyx@gmail.com','N/A','Onyxx','Y');
insert into login(name,email,usn,passwd,eh) values('UCSP','UCSP@gmail.com','N/A','UCSPP','Y');
