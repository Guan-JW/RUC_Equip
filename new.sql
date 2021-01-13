set names utf8;
DROP DATABASE Equipment;
create DATABASE Equipment;
use Equipment;

CREATE TABLE IF NOT EXISTS `user` (
  `userid` varchar(64) PRIMARY KEY,
  `password` varchar(64) NOT NULL,
  `group` enum('1','2','3') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table Course(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    details VARCHAR(100)
)engine=InnoDB default charset=utf8;

create table Teacher(
    userid VARCHAR(64) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    course_id INTEGER,
    title_type VARCHAR(10),
    gender CHAR(2),
    email VARCHAR(30),
    FOREIGN KEY(course_id) REFERENCES Course(id) ON UPDATE CASCADE
)engine=InnoDB default charset=utf8;

create table Student(
    userid VARCHAR(64) PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    session CHAR(4),
    gender CHAR(2),
    email varchar(30)
)engine=InnoDB default charset=utf8;

create table SC(
    student_id VARCHAR(64),
    course_id INTEGER,
    PRIMARY KEY(student_id,course_id),
    FOREIGN KEY(course_id) REFERENCES Course(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(student_id) REFERENCES Student(userid) ON UPDATE CASCADE ON DELETE CASCADE
)engine=InnoDB default charset=utf8;

create table Equip(
    equip_id VARCHAR(64) PRIMARY KEY,
    equip_name VARCHAR(50),
    type VARCHAR(50),
    address VARCHAR(50),
    description VARCHAR(200),
    qualification VARCHAR(50),
    check_qualification ENUM('是','否'),
    buy_date DATE,
    status ENUM('正常','故障') default '正常'
)engine=InnoDB default charset=utf8;

insert into Equip values('-1','仪器不存在','仪器不存在','仪器不存在','仪器不存在','仪器不存在','否','2020-11-11','故障');

create table EquipManager(
    manager_id VARCHAR(64) PRIMARY KEY,
    name  VARCHAR(20),
    email VARCHAR(30)
)engine=InnoDB default charset=utf8;

create table Equip_Manage(
    equip_id VARCHAR(64),
    manager_id VARCHAR(64),
    PRIMARY KEY(equip_id,manager_id),
    FOREIGN KEY(equip_id) REFERENCES Equip(equip_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(manager_id) REFERENCES EquipManager(manager_id) ON UPDATE CASCADE ON DELETE CASCADE
)engine=InnoDB default charset=utf8;

create table Appointment(
    appointment_id INTEGER,
    use_time INTEGER,
    use_date DATE,
    PRIMARY KEY(appointment_id)
)engine=InnoDB default charset=utf8;

ALTER TABLE `appointment` CHANGE `appointment_id` `appointment_id` INT NOT NULL AUTO_INCREMENT;
ALTER TABLE `appointment` ADD INDEX date_index (use_date);

create table Appoint_index(
    index_id INTEGER PRIMARY KEY,
    start_id INTEGER,
    end_id INTEGER,
    userid VARCHAR(64),
    equip_id VARCHAR(64),
    course_id INTEGER,
    item VARCHAR(200),
    status ENUM('-4','-3','-2','-1','0','1','2'),
    FOREIGN KEY(start_id) REFERENCES Appointment(appointment_id) ON UPDATE CASCADE,
    FOREIGN KEY(end_id) REFERENCES Appointment(appointment_id) ON UPDATE CASCADE,
    FOREIGN KEY(userid) REFERENCES Student(userid) ON UPDATE CASCADE,
    FOREIGN KEY(equip_id) REFERENCES Equip(equip_id) ON UPDATE CASCADE,
    FOREIGN KEY(course_id) REFERENCES Course(id) ON UPDATE CASCADE
)engine=InnoDB default charset=utf8;

ALTER TABLE `Appoint_index` CHANGE `index_id` `index_id` INT NOT NULL AUTO_INCREMENT;

create table Equip_Log(
    log_id INTEGER PRIMARY KEY,
    equip_id VARCHAR(64),
    appoint_id INTEGER,
    course_id INTEGER,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    userid VARCHAR(64),
    item VARCHAR(50),
    e_status ENUM('正常','故障'),
    details VARCHAR(200), 
    log_status ENUM('未完成','已提交'),
    FOREIGN KEY(equip_id) REFERENCES Equip(equip_id) ON UPDATE CASCADE,
    FOREIGN KEY(userid) REFERENCES Student(userid) ON UPDATE CASCADE,
    FOREIGN KEY(course_id) REFERENCES Course(id) ON UPDATE CASCADE,
    FOREIGN KEY(appoint_id) REFERENCES Appoint_index(index_id) ON UPDATE CASCADE
)engine=InnoDB default charset=utf8;

ALTER TABLE `Equip_Log` CHANGE `log_id` `log_id` INT NOT NULL AUTO_INCREMENT;

create table Qualification(
    userid VARCHAR(64),
    equip_id VARCHAR(64),
    PRIMARY KEY(userid,equip_id),
    FOREIGN KEY(userid) REFERENCES Student(userid) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(equip_id) REFERENCES Equip(equip_id) ON UPDATE CASCADE ON DELETE CASCADE
)engine=InnoDB default charset=utf8;


DELIMITER $$
CREATE TRIGGER FaultCheck
AFTER UPDATE ON Equip_Log
FOR EACH ROW
BEGIN 
    IF NEW.log_status='已提交'and NEW.e_status='故障' THEN
        UPDATE Equip
        SET status='故障'
        WHERE equip_id = NEW.equip_id;
    END IF;
END$$

DELIMITER $$
CREATE TRIGGER StatusCheck
AFTER UPDATE ON Equip
FOR EACH ROW
BEGIN 
    IF NEW.status='故障' THEN
        UPDATE Appoint_index
        SET status='-3'
        WHERE equip_id = NEW.equip_id;
    END IF;
END$$


DELIMITER $$
CREATE TRIGGER DeleteEquip
BEFORE DELETE ON Equip
FOR EACH ROW
BEGIN 
    UPDATE Appoint_index
    SET equip_id = '-1' 
    WHERE equip_id = OLD.equip_id;
END$$

DELIMITER $$
CREATE TRIGGER DeleteEquip1
BEFORE DELETE ON Equip
FOR EACH ROW
BEGIN 
    UPDATE Appoint_index
    SET status = '-3' 
    WHERE equip_id = OLD.equip_id;
END$$

DELIMITER $$
CREATE TRIGGER DeleteEquip2
BEFORE DELETE ON Equip
FOR EACH ROW
BEGIN 
    UPDATE Equip_Log 
    SET equip_id = '-1' 
    WHERE equip_id = OLD.equip_id;
END$$

DELIMITER $$
CREATE TRIGGER WithDraw
AFTER UPDATE ON Appoint_index
FOR EACH ROW
BEGIN 
    IF NEW.status = '-4' THEN
        DELETE
        FROM Equip_Log
        WHERE appoint_id = NEW.index_id;
    END IF;
END$$

DELIMITER $$
CREATE TRIGGER Check_Qua
AFTER UPDATE ON Equip
FOR EACH ROW
BEGIN 
    IF OLD.check_qualification= '是'  and NEW.check_qualification= '否'  THEN
        DELETE
        FROM Qualification
        WHERE equip_id = NEW.equip_id;
    END IF;
END$$

DELIMITER // 
create procedure del_data()
BEGIN
    DELETE FROM `Appoint_index` WHERE created_on < DATE_SUB(CURDATE(),INTERVAL 30 DAY);
END//
DELIMITER ;

DELIMITER // 
create procedure del_data2()
BEGIN
    DELETE FROM `Appointment` WHERE created_on < DATE_SUB(CURDATE(),INTERVAL 30 DAY);
END//
DELIMITER ;

DELIMITER // 
create procedure del_data1()
BEGIN
    DELETE FROM `Equip_Log`WHERE created_on < DATE_SUB(CURDATE(),INTERVAL 30 DAY);
END//
DELIMITER ;

SET GLOBAL event_scheduler = ON;

create event del_event  
on schedule 
EVERY 1 day  
STARTS '2020-12-4 00:00:00'  
do call del_data();

create event del_event1  
on schedule 
EVERY 1 day  
STARTS '2020-12-4 00:00:00'  
do call del_data1();

create event del_event2  
on schedule 
EVERY 1 day  
STARTS '2020-12-4 00:00:00'  
do call del_data2();

