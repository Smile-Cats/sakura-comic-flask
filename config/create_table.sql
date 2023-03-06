--------------------------评论表-------------------------------
CREATE TABLE `sakura_comment` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`body` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`reviewed` TINYINT(1) NULL DEFAULT NULL,
	`timestamp` DATETIME NULL DEFAULT NULL,
	`user_id` INT(11) NULL DEFAULT NULL,
	`replied_id` INT(11) NULL DEFAULT NULL,
	`movdetail_id` INT(11) NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `user_id` (`user_id`) USING BTREE,
	INDEX `replied_id` (`replied_id`) USING BTREE,
	INDEX `movdetail_id` (`movdetail_id`) USING BTREE,
	INDEX `ix_sakura_comment_timestamp` (`timestamp`) USING BTREE,
	CONSTRAINT `sakura_comment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `movie`.`sakura_user` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `sakura_comment_ibfk_2` FOREIGN KEY (`replied_id`) REFERENCES `movie`.`sakura_comment` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `sakura_comment_ibfk_3` FOREIGN KEY (`movdetail_id`) REFERENCES `movie`.`sakura_movdetail` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=86
;


--------------------------视频详情信息----------------------------
CREATE TABLE `sakura_movdetail` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`group_id` INT(11) NULL DEFAULT NULL,
	`type_id` INT(11) NULL DEFAULT NULL,
	`type_id_1` INT(11) NULL DEFAULT NULL,
	`type_name` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_actor` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_area` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_author` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_behind` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_blurb` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_class` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_color` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_content` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_copyright` INT(11) NULL DEFAULT NULL,
	`vod_director` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_douban_id` INT(11) NULL DEFAULT NULL,
	`vod_douban_score` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_down` INT(11) NULL DEFAULT NULL,
	`vod_down_from` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_down_note` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_down_server` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_down_url` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_duration` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_en` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_hits` INT(11) NULL DEFAULT NULL,
	`vod_hits_day` INT(11) NULL DEFAULT NULL,
	`vod_hits_month` INT(11) NULL DEFAULT NULL,
	`vod_hits_week` INT(11) NULL DEFAULT NULL,
	`vod_id` INT(11) NOT NULL,
	`vod_isend` INT(11) NULL DEFAULT NULL,
	`vod_jumpurl` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_lang` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_letter` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_level` INT(11) NULL DEFAULT NULL,
	`vod_lock` INT(11) NULL DEFAULT NULL,
	`vod_name` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pic` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pic_screenshot` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pic_slide` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pic_thumb` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_play_from` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_play_note` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_play_server` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_play_url` LONGTEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_plot` INT(11) NULL DEFAULT NULL,
	`vod_plot_detail` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_plot_name` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_points` INT(11) NULL DEFAULT NULL,
	`vod_points_down` INT(11) NULL DEFAULT NULL,
	`vod_points_play` INT(11) NULL DEFAULT NULL,
	`vod_pubdate` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pwd` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pwd_down` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pwd_down_url` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pwd_play` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pwd_play_url` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_pwd_url` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_rel_art` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_rel_vod` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_remarks` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_reurl` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_score` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_score_all` INT(11) NULL DEFAULT NULL,
	`vod_score_num` INT(11) NULL DEFAULT NULL,
	`vod_serial` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_state` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_status` INT(11) NULL DEFAULT NULL,
	`vod_sub` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_tag` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_time` DATETIME NULL DEFAULT NULL,
	`vod_time_add` INT(11) NULL DEFAULT NULL,
	`vod_time_hits` INT(11) NULL DEFAULT NULL,
	`vod_time_make` INT(11) NULL DEFAULT NULL,
	`vod_total` INT(11) NULL DEFAULT NULL,
	`vod_tpl` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_tpl_down` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_tpl_play` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_trysee` INT(11) NULL DEFAULT NULL,
	`vod_tv` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_up` INT(11) NULL DEFAULT NULL,
	`vod_version` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_weekday` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_writer` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_year` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`id`, `vod_id`) USING BTREE,
	INDEX `type_id` (`type_id`) USING BTREE,
	CONSTRAINT `sakura_movdetail_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `movie`.`sakura_movtype` (`type_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=71185
;

--------------------------------------视频信息【详情信息的简略版】--------------------------------------------------------------
CREATE TABLE `sakura_movinfo` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`type_id` INT(11) NULL DEFAULT NULL,
	`type_name` VARCHAR(20) NOT NULL COLLATE 'utf8mb4_general_ci',
	`vod_en` TEXT NOT NULL COLLATE 'utf8mb4_general_ci',
	`vod_id` INT(11) NOT NULL,
	`vod_name` TEXT NOT NULL COLLATE 'utf8mb4_general_ci',
	`vod_play_from` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_remarks` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`vod_time` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`, `vod_id`) USING BTREE,
	INDEX `type_id` (`type_id`) USING BTREE,
	CONSTRAINT `sakura_movinfo_ibfk_1` FOREIGN KEY (`type_id`) REFERENCES `movie`.`sakura_movtype` (`type_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=63781
;

--------------------------------------视频类目-----------------------------------------------------------------------
CREATE TABLE `sakura_movtype` (
	`type_id` INT(11) NOT NULL AUTO_INCREMENT,
	`type_name` VARCHAR(20) NOT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`type_id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=35
;


-----------------------------------------用户表-------------------------------------------------------------------------
CREATE TABLE `sakura_user` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(30) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
	`password_hash` VARCHAR(128) NULL DEFAULT NULL COLLATE 'utf8mb4_bin',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_bin'
ENGINE=InnoDB
AUTO_INCREMENT=42
;

----------------------------------用户收藏视频表----------------------------------------------------------------------
CREATE TABLE `sakura_user_collection` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`user_id` INT(11) NULL DEFAULT NULL,
	`movdetail_id_list` LONGTEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `user_id` (`user_id`) USING BTREE,
	CONSTRAINT `sakura_user_collection_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `movie`.`sakura_user` (`id`) ON UPDATE RESTRICT ON DELETE RESTRICT
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=11
;