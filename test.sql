create database mysql_shiyan character set UTF8;

use mysql_shiyan;

create table emp
(
  empno int primary key auto_increment,
  ename varchar(20),
  job varchar(20),
  mgr int,
  hiredate date,
  sal double(7,2),
  commit double(5,2),
  deptno int not null
);


create table dept
(
  deptno int primary key,
  dname varchar(20),
  loc varchar(20)
);


INSERT INTO emp VALUES
(1002,'zhantang','clerk',1001,'1983-05-09',7000.00,200.00,10),
(1003,'dazui','clerk',1002,'1980-07-08',8000.00,100.00,10),
(1004,'xiucai','clerk',1002,'1985-11-12',4000.00,null,10),
(1005,'furong','clerk',1002,'1985-03-04',4000.00,null,10),
(2001,'yifei','leader',null,'1994-03-04',15000.00,NULL,20),
(2002,'meijia','manger',2001,'1993-05-24',10000.00,300.00,20),
(2003,'ziqiao','clerk',2002,'1995-05-19',7300.00,100.00,20),
(2004,'zhangwei','clerk',2002,'1994-10-12',8000.00,500.00,20),
(2005,'xiaoxian','clerk',2002,'1993-05-10',9000.00,700.00,20),
(3001,'liumei','leader',null,'1968-08-08',13000.00,NULL,30),
(3002,'dongmei','manger',3001,'1968-09-21',10000.00,600.00,30),
(3003,'xiaxue','clerk',3002,'1989-09-21',8000.00,300.00,30),
(3004,'yishan','clerk',3002,'1991-06-16',88000.00,200.00,30);


INSERT INTO dept VALUES
(10,'canyinbu','shanghai'),
(20,'xiaoshoubu','zhejiang'),
(30,'caiwubu','beijing'),
(40,'jishubu','shenzhen');
