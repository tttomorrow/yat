#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <ctype.h>
#include <assert.h>
#include <errno.h>

#include <sql.h>
#include <sqlext.h>

#ifdef WIN32
#include <windows.h>
#endif

#define KEY_VAL_LEN 100




char *l_trim(char * szOutput, const char *szInput);
char *r_trim(char *szOutput, const char *szInput);
char *a_trim(char * szOutput, const char * szInput);
int GetProfileVal(char *profile, char *AppName, char *KeyName, char *KeyVal);

SQLRETURN  ret    = 0;                     // Return value
SQLINTEGER erg    = 0;
SQLINTEGER err    = 0;
SQLINTEGER id     = 1;                     // id value

SQLCHAR     *SqlState       = NULL;
SQLINTEGER  *NativeErrorPtr = NULL;
SQLCHAR     *buffer         = NULL;        // Resultset Buffer
SQLSMALLINT *TextLengthPtr  = NULL;

SQLHENV   Env_Handle;                      // Environment Handle
SQLHDBC   Dbc_Handle;                      // DB Connection Handle
SQLHSTMT  Stmt_Handle;                     // Statement Handle

char *dropSql = "drop table IF EXISTS odbc_test_tbl1;";
char *createSql = "CREATE TABLE odbc_test_tbl1(id INTEGER, name VARCHAR(32));";
char *prepareSql = "insert into odbc_test_tbl1 values(?, ?);";
char *selectSql = "select * from odbc_test_tbl1;";

char *name = "Jack";

char *columnName = "id";

int main(void)
{

    char user[20] = { 0 };
    char password[20] = { 0 };

    GetProfileVal("/etc/odbc.ini", "gaussodbc", "Username", user);
    GetProfileVal("/etc/odbc.ini", "gaussodbc", "Password", password);


    // Alloc Environment Handle
    ret = SQLAllocHandle(SQL_HANDLE_ENV, SQL_NULL_HANDLE, &Env_Handle);
    if ((ret != SQL_SUCCESS) &&
        (ret != SQL_SUCCESS_WITH_INFO)) {
        printf("Environment Handle : Alloc Error!\n");
        exit(0);
        return 0;
    }
    printf("Environment Handle : Alloc Success!\n");


    // Set Environment Attribute
    ret = SQLSetEnvAttr(Env_Handle, SQL_ATTR_ODBC_VERSION, (SQLPOINTER)SQL_OV_ODBC3, 0);
    if ((ret != SQL_SUCCESS) &&
        (ret != SQL_SUCCESS_WITH_INFO)) {
        printf("Environment Attribute : Set Error!\n");

        SQLFreeHandle(SQL_HANDLE_ENV, Env_Handle);
        printf("Environment Handle : Free Success!\n");

        exit(0);
        return 0;
    }
    printf("Environment Attribute : Set Success!\n\n");


    // Alloc DB Connect Handle
    ret = SQLAllocHandle(SQL_HANDLE_DBC, Env_Handle, &Dbc_Handle);
    if ((ret != SQL_SUCCESS) &&
        (ret != SQL_SUCCESS_WITH_INFO)) {
        printf("DB Connect Handle : Alloc Error!\n");

        SQLFreeHandle(SQL_HANDLE_ENV, Env_Handle);
        printf("Environment Handle : Free Success!\n");

        exit(0);
        return 0;
    }
    printf("DB Connect Handle : Alloc Success!\n");


    // Set Connect Attribute
    ret = SQLSetConnectAttr(Dbc_Handle, SQL_ATTR_AUTOCOMMIT, (SQLPOINTER)SQL_AUTOCOMMIT_ON, 0);
    if ((ret != SQL_SUCCESS) &&
        (ret != SQL_SUCCESS_WITH_INFO)) {
        printf("Connect Attribute : Set Error!\n");

        SQLFreeHandle(SQL_HANDLE_DBC, Dbc_Handle);
        printf("DB Connect Handle : Free Success!\n");

        SQLFreeHandle(SQL_HANDLE_ENV, Env_Handle);
        printf("Environment Handle : Free Success!\n");

        exit(0);
        return 0;
    }
    printf("DB Connect Attribute : Set Success!\n");


    // Connect DB Source
    ret = SQLConnect(Dbc_Handle,
                     (SQLCHAR *) "gaussodbc", SQL_NTS,
                     (SQLCHAR *) user, SQL_NTS,
                     (SQLCHAR *) password, SQL_NTS);
    if ((ret != SQL_SUCCESS) &&
        (ret != SQL_SUCCESS_WITH_INFO)) {
        printf("DB Source : Connect Error!\n");

        SQLFreeHandle(SQL_HANDLE_DBC, Dbc_Handle);
        printf("DB Connect Handle : Free Success!\n");

        SQLFreeHandle(SQL_HANDLE_ENV, Env_Handle);
        printf("Environment Handle : Free Success!\n");

        exit(0);
        return 0;
    }
    printf("DB Source : Connect Success!\n\n");


    // Alloc Statement Handle
    ret = SQLAllocHandle(SQL_HANDLE_STMT, Dbc_Handle, &Stmt_Handle);
    if ((ret != SQL_SUCCESS) &&
        (ret != SQL_SUCCESS_WITH_INFO)) {
        printf("Statement Handle : Alloc Error!\n");

        SQLDisconnect(Dbc_Handle);
        printf("DB Connect : Disconnect Success!\n");

        SQLFreeHandle(SQL_HANDLE_DBC, Dbc_Handle);
        printf("DB Connect Handle : Free Success!\n");

        SQLFreeHandle(SQL_HANDLE_ENV, Env_Handle);
        printf("Environment Handle : Free Success!\n");

        exit(0);
        return 0;
    }
    printf("Statement Handle : Alloc Success!\n");


    // Set Statement Attribute
    ret = SQLSetStmtAttr(Stmt_Handle, SQL_ATTR_QUERY_TIMEOUT, (SQLPOINTER)3, 0);
    if ((ret != SQL_SUCCESS) &&
        (ret != SQL_SUCCESS_WITH_INFO)) {
        printf("Statement Attribute : Set Error!\n");

        SQLFreeHandle(SQL_HANDLE_STMT, Stmt_Handle);
        printf("Statement Handle : Free Success!\n");

        SQLDisconnect(Dbc_Handle);
        printf("DB Connect : Disconnect Success!\n");

        SQLFreeHandle(SQL_HANDLE_DBC, Dbc_Handle);
        printf("DB Connect Handle : Free Success!\n");

        SQLFreeHandle(SQL_HANDLE_ENV, Env_Handle);
        printf("Environment Handle : Free Success!\n");

        exit(0);
        return 0;
    }
    printf("Statement Attribute : Set Success!\n\n");


    // Execute SQL
    SQLExecDirect(Stmt_Handle, (SQLCHAR *)createSql, SQL_NTS);
    printf("SQLExecDirect() : Create Table Success!\n\n");


    // Prepare SQL
    SQLPrepare(Stmt_Handle, (SQLCHAR *)prepareSql, SQL_NTS);
    printf("SQLPrepare() : Prepare Success!\n");

    // Bind Parameter
    SQLBindParameter(Stmt_Handle, 1, SQL_PARAM_INPUT, SQL_C_SLONG, SQL_INTEGER, 0, 0, &id, 0, NULL);
    SQLBindParameter(Stmt_Handle, 2, SQL_PARAM_INPUT, SQL_C_CHAR, SQL_CHAR, 0, 0, name, 0, NULL);
    printf("SQLBindParameter() : Bind Parameter Success!\n");

    // Execute Prepare SQL
    SQLExecute(Stmt_Handle);
    printf("SQLExecute() : Execute Prepare SQL Success!\n\n");

    // Execute Select SQL
    SQLExecDirect(Stmt_Handle, (SQLCHAR *)selectSql, SQL_NTS);
    printf("SQLExecDirect() : Select Success!\n");
	
	// Execute Drop SQL
	SQLExecDirect(Stmt_Handle, (SQLCHAR *)dropSql, SQL_NTS);
    printf("SQLExecDirect() : Drop Table Success!\n");

    // Get Data Column Resultset
    SQLColAttribute(Stmt_Handle, 1, SQL_DESC_TYPE, columnName, 100, NULL, NULL);
    printf("SQLColAttribute() : Call Success!\n");
    printf("Data Column Name : %s\n", columnName);

    SQLBindCol(Stmt_Handle, 1, SQL_C_SLONG, (SQLPOINTER)buffer, 150, (SQLLEN *)&err);
    printf("SQLBindCol() : Call Success!\n");
    erg = SQLFetch(Stmt_Handle);
    while (erg != SQL_NO_DATA) {
        SQLGetData(Stmt_Handle, 1, SQL_C_SLONG, (SQLPOINTER)&id, 0, NULL);
        printf("Data(id) : %d\n", id);
        erg = SQLFetch(Stmt_Handle);
    }
    printf("Data Query Success!\n");
    printf("SQLFetch() : Call Success!\n");
    printf("SQLGetData() : Call Success!\n\n");


    SQLGetDiagRec(SQL_HANDLE_STMT, Stmt_Handle, 1, (SQLCHAR *)SqlState, NativeErrorPtr, buffer, 1000, TextLengthPtr);
    printf("SQLGetDiagRec() : Call Success!\n");
    printf("  SQLState       : %x\n", SqlState);
    printf("  NativeErrorPtr : %x\n", NativeErrorPtr);
    printf("  TextLengthPtr  : %d\n\n", TextLengthPtr);


    // Free Handle
    SQLFreeHandle(SQL_HANDLE_STMT, Stmt_Handle);
    printf("Statement Handle : Free Success!\n");

    SQLDisconnect(Dbc_Handle);
    printf("DB Connect : Disconnect Success!\n");

    SQLFreeHandle(SQL_HANDLE_DBC, Dbc_Handle);
    printf("DB Connect Handle : Free Success!\n");

    SQLFreeHandle(SQL_HANDLE_ENV, Env_Handle);
    printf("Environment Handle : Free Success!\n");

    return 0;
}


char *l_trim(char * szOutput, const char *szInput)
{
    assert(szInput != NULL);
    assert(szOutput != NULL);
    assert(szOutput != szInput);
    for (NULL; *szInput != '\0' && isspace(*szInput); ++szInput) {
        ;
    }
    return strcpy(szOutput, szInput);
}

char *r_trim(char *szOutput, const char *szInput)
{
    char *p = NULL;
    assert(szInput != NULL);
    assert(szOutput != NULL);
    assert(szOutput != szInput);
    strcpy(szOutput, szInput);
    for (p = szOutput + strlen(szOutput) - 1; p >= szOutput && isspace(*p); --p) {
        ;
    }
    *(++p) = '\0';
    return szOutput;
}

char *a_trim(char * szOutput, const char * szInput)
{
    char *p = NULL;
    assert(szInput != NULL);
    assert(szOutput != NULL);
    l_trim(szOutput, szInput);
    for (p = szOutput + strlen(szOutput) - 1;p >= szOutput && isspace(*p); --p) {
        ;
    }
    *(++p) = '\0';
    return szOutput;
}

int GetProfileVal(char *profile, char *AppName, char *KeyName, char *KeyVal)
{
    char appname[32], keyname[32];
    char *buf, *c;
    char buf_i[KEY_VAL_LEN], buf_o[KEY_VAL_LEN];
    FILE *fp;
    int found = 0;
	if ((fp = fopen(profile, "r")) == NULL) {
        printf("openfile [%s] error [%s]\n", profile, strerror(errno));
        return(-1);
    }
    fseek(fp, 0, SEEK_SET);
    memset(appname, 0, sizeof(appname));
    sprintf(appname, "[%s]", AppName);

    while (!feof(fp) && fgets(buf_i, KEY_VAL_LEN, fp) != NULL) {
        l_trim(buf_o, buf_i);
        if (strlen(buf_o) <= 0)
            continue;
        buf = NULL;
        buf = buf_o;

        if (found == 0) {
            if (buf[0] != '[') {
                continue;
            }
            else if (strncmp(buf, appname, strlen(appname)) == 0) {
                found = 1;
                continue;
            }

        }
        else if (found == 1) {
            if (buf[0] == '#') {
                continue;
            }
            else if (buf[0] == '[') {
                break;
            }
            else {
                if ((c = (char*)strchr(buf, '=')) == NULL)
                    continue;
                memset(keyname, 0, sizeof(keyname));

                sscanf(buf, "%[^=|^ |^\t]", keyname);
                if (strcmp(keyname, KeyName) == 0) {
                    sscanf(++c, "%[^\n]", KeyVal);
                    char *KeyVal_o = (char *)malloc(strlen(KeyVal) + 1);
                    if (KeyVal_o != NULL) {
                        memset(KeyVal_o, 0, sizeof(KeyVal_o));
                        a_trim(KeyVal_o, KeyVal);
                        if (KeyVal_o && strlen(KeyVal_o) > 0) {
                            strcpy(KeyVal, KeyVal_o);
                        }
                        free(KeyVal_o);
                        KeyVal_o = NULL;
                    }
                    found = 2;
                    break;
                }
                else {
                    continue;
                }
            }
        }
    }
    fclose(fp);
    if (found == 2) {
        return(0);
    }
    else {
        return(-1);
    }
}