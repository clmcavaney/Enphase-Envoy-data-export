CREATE TABLE `envoy_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(16) NOT NULL,
  `timestamp` timestamp NOT NULL,
  `p_e_whToday` decimal(8,3) NOT NULL DEFAULT '-1.0',
  `p_e_whLifetime` decimal(10,3) NOT NULL DEFAULT '-1.0',
  `p_p_wnow` decimal(8,3) NOT NULL DEFAULT '-1.0',
  `p_v_rms` decimal(6,3) NOT NULL DEFAULT '-1.0',
  `p_pwr_f` decimal(4,1) NOT NULL DEFAULT '-1.0',
  `c_e_whToday` decimal(8,3) NOT NULL DEFAULT '-1.0',
  `c_e_whLifetime` decimal(10,3) NOT NULL DEFAULT '-1.0',
  `c_p_wnow` decimal(8,3) NOT NULL DEFAULT '-1.0',
  `c_v_rms` decimal(6,3) NOT NULL DEFAULT '-1.0',
  `c_pwr_f` decimal(4,1) NOT NULL DEFAULT '-1.0',
  `ServerStamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)
