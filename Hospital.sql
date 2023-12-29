create table General_Department(
Dnumber serial UNIQUE,
Dname varchar(20)

);

create table Doctor(
DID serial UNIQUE ,
DSSN varchar(14) UNIQUE not NULL,
DFname varchar(20) not NULL,
DLname varchar(20) not NULL,
DEmail varchar(100) UNIQUE not null,
ppassword varchar(30) not null,
Dbirthdate date not NULL,
Daddress varchar(100) not NULL,
Dphone varchar(20) not NULL,
Dgender varchar(1) CHECK ( Dgender='F' OR Dgender='M' ),
Deducation varchar(100) not NULL,
Dsalary int  not NULL,
specialization varchar(30)  not NULL,
DNo int references General_Department (Dnumber)

);


create table Manages(
Dnumber int references General_Department(Dnumber),
Mgr_Id int references Doctor (DID)
);


create table Patient (
PID SERIAL UNIQUE,
PSSN varchar(14) UNIQUE not null,
PFname varchar(20) not null,
PLname varchar(20) not null,
pEmail varchar(100) UNIQUE not null,
ppassword varchar(30) not null,
Paddress varchar(100) not null,
Pbirthdate date not null,
Pgender varchar(1) CHECK ( Pgender='F' OR  Pgender='M' ),
Pphone varchar(20) not null,
medical_history varchar(300),
medical_status varchar(300)
);

create table Nurse(
NID SERIAL UNIQUE,
NSSN varchar(14) UNIQUE not null,
NFname varchar(20) not null,
NLname varchar(20) not null,
Nbirthdate date not null,
Naddress varchar(100) not null,
Nphone varchar(20) not null,
Ngender varchar(1) CHECK ( Ngender='F' OR Ngender='M' ),
Neducation varchar(1000) not null,
salary int not null,
DNo int references General_Department (Dnumber)

);


create table ICU(
DNo int references General_Department (Dnumber),
capacity int  not null,
severity varchar(50) not null
 );

create table Surgery(
DNo int references General_Department (Dnumber),
type varchar(50) not null
);

create table Scan(
SID serial UNIQUE,
CT bool,
XRAY bool,
MRI bool,
SDate date  not null

);

create table Medical_Equipment(
DNo int references General_Department (Dnumber),
Equipment varchar(200) not null

);

create table Medication(
M_id serial UNIQUE,
dose varchar(30)  not null,
Mname varchar(50),
timing time  not null,
startdate date  not null,
enddate date  not null
);

create table Takes(
Pid int references Patient (PID),
Mid int references Medication (M_id)
);

create table Examines(
Pid int references Patient (PID),
Did int references Doctor (DID)
);

create table Performs(
Pid int references Patient (PID),
Sid int references Scan (SID)
);

create table Enters(
Pid int references Patient (PID),
DNo int references General_department (Dnumber),
leavedate date not null,
startdate date not null
);

create table Cares_for(
Pid int references Patient (PID),
Nid int references Nurse (NID)
);

create table Prescribes(
Mid int references Medication (M_id),
Did int references Doctor (DID)
);