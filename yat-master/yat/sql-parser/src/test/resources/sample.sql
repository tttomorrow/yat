@conn xxx/passwd@127.0.0.1:9090;
drop table if exists tbl_x;

create table tbl_x (id int, age int, xb int);

insert into tbl_x values(1, 2, 4);
insert into tbl_x values(3, 4, 5);

insert into tbl_x values(?, ?, ?);
@bind {
    int 3
    int 5
    int 7
}
select * from tbl_x;

insert into tbl_x values(?, ?, ?);
@batch {
    int 3 int 4 int 0
    int 3 int 4 int 9
    int 3 int 4 int 8
    int 3 int 4 int 7
}

@shell command/xml_parser -t data/abc.xml;
@sh zctl.py -t stop;
@sh zctl.py -t start;

create or replace procedure proc_001 as
    v1 := 1
    v2 := 2
begin

    select * from tbl_x where id = v1;
end;
/

@async(timeout: 3s)
{
    @set autocommit false;
    select * from tbl_x for update;
    commit;
}

select * from tbl_x;


@session(name: s1)
{
    @set autocommit false;
    update table tbl_x set par1 = 2 par2 = 2;
    insert into tbl_x values(1, 3, 4);
    commit;
}

@session(name: s2, user: abc, password: '')
{
    @set autocommit false;
    update table tbl_x set par1 = 2 par2 = 2;
    insert into tbl_x values(1, 3, 4);
    @step
    {
        select * from tbl_x for update;
        select * from tbl_x;
    }
    commit;
}

@session(name: s3, host: '', port: 2345, user: abc, password: '')
{
    @set autocommit false;
    update table tbl_x set par1 = 2 par2 = 2;
    insert into tbl_x values(1, 3, 4);
    @step
    {
        select * from tbl_x for update;
        select * from tbl_x;
    }
    commit;
}

@session(name: s4, node: other_node)
{
    @set autocommit false;
    update table tbl_x set par1 = 2 par2 = 2;
    insert into tbl_x values(1, 3, 4);
    @step
    {
        select * from tbl_x for update;
        select * from tbl_x;
    }
    commit;
}

@steps s1.0 s2.0 s1.1 s1.2 s2.2 s2.1;

@steps s1.0 s2.0 s2.1 s2.2 s1.2 s1.1;

@for (count: 10)
{
    select * from abc;
    insert into abc values(1,1,3,4);
}

@stats_checker (table: abc, part: p1, check: all, compare: 0.1)
@sh yat call stats_checker --table=abc --part=xxx --check=all --compare=0.1

@parallel {
    @session {
        select * from abc for update;
        commit;
    }

    @session {
        select * from abc for update;
        commit;
    }
}