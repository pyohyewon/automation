base_url = 'http://prod.XXXXXX.co.kr/'
userEmail = 'hwpyo@XXXXXX.co.kr'
userPw = '123!@#'

msg_sql = "SELECT msg_job_cd, msg_cd, msg_txt, msg_type_cd, reg_dy FROM cpxown.tb_comm_msg01c"
corp_sql = "SELECT corp_nm, rpsv_nm, upjong_nm, etsr_no, chrg_clerk_nm, chrg_clerk_tel_no, memo_txt, cotr_start_dy, cotr_end_dy, reg_dy, upd_dy FROM cpxown.tb_comm_corp01m"
