use Test;

create table if not exists Store (
	id int AUTO_INCREMENT  primary key  not null
);

create table if not exists Camera (
	id int primary key AUTO_INCREMENT  not null,
	storeId int not null,
	foreign key(storeId) references Store(id)
);

create table if not exists Person (
	id int primary key auto_increment,
    aws_face_id varchar(50) not null
);

create table if not exists AwsIndexedPerson(
	id int primary key auto_increment,
	person_id int not null,
    aws_image_id int not null,
    foreign key (person_id) references Person(id)
);

create table if not exists PersonOccurrence (
	id int primary key auto_increment,
    store_id int not null,
    camera_id int not null,
    occurance_timestamp datetime not null,
    person_id int not null,
    foreign key(store_id) references Store(id),
	foreign key(camera_id) references Camera(id),
    foreign key(person_id) references Person(id)	
);
