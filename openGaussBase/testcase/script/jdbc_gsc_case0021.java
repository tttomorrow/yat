"""
Copyright (c) 2022 Huawei Technologies Co.,Ltd.

openGauss is licensed under Mulan PSL v2.
You can use this software according to the terms and conditions of the Mulan PSL v2.
You may obtain a copy of Mulan PSL v2 at:

          http://license.coscl.org.cn/MulanPSL2

THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
See the Mulan PSL v2 for more details.
"""
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Properties;

/**
 **/

public class jdbc_gsc_case0021 {
	static public String driver = "org.postgresql.Driver";
	static public String tb_name;
	static Properties pros_conf = null;

	public static Properties getConfigFromFile(String filePath) {
		Properties props = new Properties();
		try {
			BufferedInputStream config = new BufferedInputStream(new FileInputStream(filePath));
			props.load(config);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return props;
	}

	public static String genURLFromPro(Properties props) {
		String hostname = props.getProperty("hostname");
		String[] hostnames = hostname.split(",");
		String port = props.getProperty("port");
		String[] ports = port.split(",");
		String dbname = props.getProperty("dbname");
		tb_name = props.getProperty("tbname");
		return genURLFromHostsPortsDBname(hostnames, ports, dbname);
	}

	public static String genURLFromHostsPortsDBname(String[] hostnames, String[] ports, String dbname) {
		String sourceURL;
		if (hostnames.length == 1) {
			sourceURL = "jdbc:postgresql://" + hostnames[0] + ":" + ports[0] + "/" + dbname;
		} else {
			ArrayList<String> ip_port_pare = new ArrayList<>();
			if (ports.length == 1) {
				for (String ip : hostnames) {
					ip_port_pare.add(ip + ":" + ports[0]);
				}
			} else {
				for (int i = 0; i < hostnames.length; i++) {
					ip_port_pare.add(hostnames[i] + ":" + ports[i]);
				}
			}
			sourceURL = "jdbc:postgresql://" + String.join(",", ip_port_pare) + "/" + dbname;
		}
		return sourceURL;
	}

	public static Connection GetConnection(Properties props) {
		Connection connR;
		String sourceURL = genURLFromPro(props);
		try {
			Class.forName(driver).newInstance();
			connR = DriverManager.getConnection(sourceURL, props);
		} catch (Exception var10) {
			var10.printStackTrace();
			return null;
		}
		return connR;
	}

	public static void main(String[] args) throws InterruptedException {
		Properties pros = new Properties();
		String jdbc_config_file = null;
		for (int i = 0; i < args.length; i++) {
			switch (args[i]) {
			case "--config-file":
				jdbc_config_file = args[i + 1];
				pros_conf = getConfigFromFile(jdbc_config_file);
				break;
			case "-F":
				jdbc_config_file = args[i + 1];
				pros_conf = getConfigFromFile(jdbc_config_file);
				break;
			default:
				break;
			}
		}
		if (pros_conf != null) {
			pros_conf.putAll(pros);
			for (int i = 0; i < 100; i++) {
				Thread s = new select_Thread();
				s.start();
			}
			for (int i = 0; i < 50; i++) {
				Thread t = new DDL_Thread();
				t.start();
				t.join();
			}
		}
	}
}

class select_Thread extends Thread {
	public void run() {
		System.out.println("select thread");
		Connection connection = null;
		Statement statement = null;
		try {
			connection = jdbc_gsc_case0021.GetConnection(jdbc_gsc_case0021.pros_conf);
			statement = connection.createStatement();
			for (int i = 0; i < 10000; i++) {
				statement.executeQuery("select * from " + jdbc_gsc_case0021.tb_name + ";");
			}
			System.out.println("查询线程" + Thread.currentThread().getName() + "查询完成");
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			try {
				statement.close();
				connection.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		}

	}
}

class DDL_Thread extends Thread {
	public void run() {
		System.out.println("DDL thread");
		Statement statement1 = null;
		Statement statement2 = null;
		Statement statement = null;
		Connection connection = null;
		try {
			connection = jdbc_gsc_case0021.GetConnection(jdbc_gsc_case0021.pros_conf);
			connection.setAutoCommit(false);
			statement = connection.createStatement();
			statement1 = connection.createStatement();
			statement2 = connection.createStatement();

			statement1.execute("alter table " + jdbc_gsc_case0021.tb_name + " add column bak1 char(40);");
			connection.commit();
			try {
				statement.executeQuery("select bak1 from " + jdbc_gsc_case0021.tb_name + ";");
				System.out.println("增加字段" + Thread.currentThread().getName() + "查询成功");
			} catch (SQLException e) {
				System.out.println("异常：增加字段" + Thread.currentThread().getName() + "查询失败");
			}
			statement2.execute("alter table " + jdbc_gsc_case0021.tb_name + " drop column bak1;");
			connection.commit();
			try {
				statement.executeQuery("select bak1 from " + jdbc_gsc_case0021.tb_name + ";");
				System.out.println("异常：删除字段" + Thread.currentThread().getName() + "查询成功");
			} catch (SQLException e) {
				System.out.println("删除字段" + Thread.currentThread().getName() + "查询失败");
			}
		} catch (SQLException e) {
			e.printStackTrace();

		} finally {
			try {
				statement1.close();
				statement2.close();
				connection.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
		}
	}
}
