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
    student_id int,
    time_placed varchar(100),
    foreign key (item_id) references items(id) on delete cascade,
    primary key (id)
);