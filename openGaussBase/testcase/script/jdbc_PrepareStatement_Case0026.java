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
import java.sql.*;
import java.util.ArrayList;
import java.util.Properties;

/**
 **/

public class jdbc_PrepareStatement_Case0026 {
	static public String driver = "org.postgresql.Driver";
	static public String tb_name;
	static public int insert_num = 0;

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
		System.out.println(sourceURL);
		try {
			Class.forName(driver).newInstance();
			connR = DriverManager.getConnection(sourceURL, props);
		} catch (Exception var10) {
			var10.printStackTrace();
			return null;
		}
		return connR;
	}

	public static void main(String[] args) {
		Properties pros = new Properties();
		Properties pros_conf = null;
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
			Connection conn = GetConnection(pros_conf);
			PreparedStatement stmt_insert = null;
			try {
				for (int i = 0; i < 10; i++) {
					stmt_insert = conn.prepareStatement("insert into " + tb_name + " values(11, '1a', 11)");
					stmt_insert.executeUpdate();
					insert_num++;
					System.out.println(insert_num);
					stmt_insert.close();
					stmt_insert.close();
				}
			} catch (SQLException e) {
				e.printStackTrace();
			} finally {
				try {
					if (insert_num == 10) {
						System.out.println("插入成功");
					}
					stmt_insert.close();
					conn.close();
				} catch (SQLException e) {
					e.printStackTrace();
				}
			}

		}
	}
}