@random
{
    select * from gcc;
    analyze table gcc;
}
@inject(sleep: '0, 200')
{
    @sh kill_db;
}
@checker
{
    @sh check_core;
    @sh check_db;
}
