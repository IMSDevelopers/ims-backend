create table if not exists items (
    id int not null primary key auto_increment,
    name varchar (30),
    quantity int,
    description text,
    url_image text,
);

create table if not exists orders (
    id int not null auto_increment,
    order_id int,
    item_id int,
    num_ordered int,
    student_id varchar(6),
    order_status ENUM('rejected', 'pending', 'accepted'),
    foreign key (item_id) references items(id) on delete cascade,
    primary key (id)
);