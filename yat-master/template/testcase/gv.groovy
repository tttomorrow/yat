import junit.*


class gv {
    @Inject
    Context ctx

    @Before
    def before() {

    }

    @Test
    def test_load() {
        ctx.sql("select * from v\$lock")
    }

    @Test
    def test_load_and_dump() {
        ctx.sql("select * from user_tables")
    }

    @Test
    def test_all() {

    }
}