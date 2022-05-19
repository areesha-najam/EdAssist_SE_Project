CREATE TABLE Parents (
    ParentID varchar(255),
    ParentName varchar(255),
    Password varchar(255),
    StudentID varchar(255)
);
--CREATE TABLE Courses (
--    CourseID varchar(255),
--    CourseName varchar(255)
--);
--CREATE TABLE Students_has_courses (
--    StudentID varchar(255),
--    CourseID varchar(255)
--);
--CREATE TABLE Student(
--    StudentID varchar(255),
--    StudentName varchar(255)
--);



INSERT INTO Parents(ParentID,ParentName,Password, StudentID)
VALUES ('sa06132','Saad Ahmed','abc123','aa001'),
       ('sf06199','Sana Fatima','aa123','ba002'),
	    ('sk06232','Sahil Khan','hj8989','da003'),
       ('af06899','Affab Fareed','kk123','jk004'),
	    ('ba06142','Basim Ali','fgh123','az005'),
       ('zf06177','Zia Faraz','bb153','la006'),
	    ('kk06252','Kashan Khan','hj8889','lj007'),
       ('gf06839','Gazal Farhan','kk333','jk008'),
	    ('ja06442','Jasmine Ali','fgh000','fa009'),
       ('hf06444','Hafsa Fariz','bb003','ad010')


INSERT INTO Student(StudentID,StudentName)
VALUES ('aa001','Ashar Ahmed'),
       ('ba002','Badae Aslam'),
	    ('da003','Dania Ahmed'),
       ('jk004','Javeria Khan'),
	   ('az005','Atif Zia'),
       ('la006','Laila Asim'),
	    ('lj007','Laiba Jawaid'),
       ('jk008','Jaleel Khan'),
	    ('fa009','Faraz Ahmed'),
       ('ad010','Atif Dayan')

INSERT INTO Students_has_courses(StudentID,CourseID)
VALUES ('aa001','MATH101'),
       ('ba002','MATH101'),
	    ('da003','MATH101'),
       ('jk004','MATH101'),
	   ('az005','MATH101'),
       ('la006','MATH101'),
	    ('lj007','MATH101'),
       ('jk008','MATH101'),
	    ('fa009','MATH101'),
       ('ad010','MATH101'),
	   ('aa001','SCI101'),
       ('ba002','SCI101'),
	    ('da003','SCI101'),
       ('jk004','SCI101'),
	   ('az005','SCI101'),
       ('la006','SCI101'),
	    ('lj007','SCI101'),
       ('jk008','SCI101'),
	    ('fa009','SCI101'),
       ('ad010','SCI101'),
	   ('aa001','SCI102'),
       ('ba002','SCI102'),
	    ('da003','SCI102'),
       ('jk004','SCI102'),
	   ('az005','SCI102'),
       ('la006','SCI102'),
	    ('lj007','SCI102'),
       ('jk008','SCI102'),
	    ('fa009','SCI102'),
       ('ad010','SCI102'),
	   ('aa001','URDU101'),
       ('ba002','URDU101'),
	    ('da003','URDU101'),
       ('jk004','URDU101'),
	   ('az005','URDU101'),
       ('la006','URDU101'),
	    ('lj007','URDU101'),
       ('jk008','URDU101'),
	    ('fa009','URDU101'),
       ('ad010','URDU101'),
	    ('aa001','ENG101'),
       ('ba002','ENG101'),
	    ('da003','ENG101'),
       ('jk004','ENG101'),
	   ('az005','ENG101'),
       ('la006','ENG101'),
	    ('lj007','ENG101'),
       ('jk008','ENG101'),
	    ('fa009','ENG101'),
       ('ad010','ENG101')

INSERT INTO Courses(CourseID,CourseName)
VALUES ('MATH101','Mathematics'),
       ('SCI101','Chemistry'),
	    ('SCI102','Physics'),
       ('URDU101','Urdu'),
	    ('ENG101','English')
		
select* from Parents
select* from Student
select* from Students_has_courses
select* from Courses