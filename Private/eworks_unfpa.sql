/*
Navicat MySQL Data Transfer

Source Server         : Lessons_app
Source Server Version : 50641
Source Host           : localhost:3306
Source Database       : eworks_unfpa

Target Server Type    : MYSQL
Target Server Version : 50641
File Encoding         : 65001

Date: 2018-11-13 17:04:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `auth_key` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password_reset_token` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` smallint(6) NOT NULL DEFAULT '10',
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `password_reset_token` (`password_reset_token`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for choose_items
-- ----------------------------
DROP TABLE IF EXISTS `choose_items`;
CREATE TABLE `choose_items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `choose_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sfsdf` (`choose_id`),
  CONSTRAINT `sfsdf` FOREIGN KEY (`choose_id`) REFERENCES `choose_tests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=371 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for choose_test_res
-- ----------------------------
DROP TABLE IF EXISTS `choose_test_res`;
CREATE TABLE `choose_test_res` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  `test_id` int(11) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `xczxc` (`user_id`),
  KEY `rwh4` (`item_id`),
  KEY `ytrbgf` (`test_id`),
  CONSTRAINT `rwh4` FOREIGN KEY (`item_id`) REFERENCES `choose_items` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `xczxc` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `ytrbgf` FOREIGN KEY (`test_id`) REFERENCES `choose_tests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4831 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for choose_tests
-- ----------------------------
DROP TABLE IF EXISTS `choose_tests`;
CREATE TABLE `choose_tests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text_pop` text,
  `title` varchar(255) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for city
-- ----------------------------
DROP TABLE IF EXISTS `city`;
CREATE TABLE `city` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for community
-- ----------------------------
DROP TABLE IF EXISTS `community`;
CREATE TABLE `community` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=802 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for config
-- ----------------------------
DROP TABLE IF EXISTS `config`;
CREATE TABLE `config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for drag_lessons
-- ----------------------------
DROP TABLE IF EXISTS `drag_lessons`;
CREATE TABLE `drag_lessons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `drag_test_id` int(11) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `color` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `text` text,
  `status` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rtytryr` (`drag_test_id`),
  CONSTRAINT `rtytryr` FOREIGN KEY (`drag_test_id`) REFERENCES `drag_tests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1087 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for drag_test_res
-- ----------------------------
DROP TABLE IF EXISTS `drag_test_res`;
CREATE TABLE `drag_test_res` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `test_id` int(11) DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `global_lesson_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fhgn` (`user_id`),
  KEY `rhhuj` (`test_id`),
  KEY `dfg` (`global_lesson_id`),
  CONSTRAINT `dfg` FOREIGN KEY (`global_lesson_id`) REFERENCES `lessons_group` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fhgn` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `rhhuj` FOREIGN KEY (`test_id`) REFERENCES `drag_tests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for drag_tests
-- ----------------------------
DROP TABLE IF EXISTS `drag_tests`;
CREATE TABLE `drag_tests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text_pop` text,
  `title` varchar(255) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  `description` text,
  `text_block_1` varchar(255) DEFAULT NULL,
  `text_block_2` varchar(255) DEFAULT NULL,
  `text_block_3` varchar(255) DEFAULT NULL,
  `error_text` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for gallerys
-- ----------------------------
DROP TABLE IF EXISTS `gallerys`;
CREATE TABLE `gallerys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for hardest_age
-- ----------------------------
DROP TABLE IF EXISTS `hardest_age`;
CREATE TABLE `hardest_age` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pop_text` text,
  `title` varchar(255) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  `text_1` text,
  `text_2` text,
  `text_3` text,
  `block_1` text,
  `block_2` text,
  `block_3` text,
  `block_4` text,
  `block_5` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for hardest_age_qu
-- ----------------------------
DROP TABLE IF EXISTS `hardest_age_qu`;
CREATE TABLE `hardest_age_qu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_id` int(11) DEFAULT NULL,
  `question` text,
  `answer_1` text,
  `answer_2` text,
  `answer_3` text,
  `answer_4` text,
  `answer_5` text,
  `answer_6` text,
  `answer_7` text,
  `answer_8` text,
  `answer_9` text,
  `answer_10` text,
  `right_answers` text,
  `img` text,
  `question_1` text,
  `question_2` text,
  `question_3` text,
  `question_4` text,
  `question_5` text,
  `question_6` text,
  `question_7` text,
  `question_8` text,
  `question_9` text,
  `question_10` text,
  PRIMARY KEY (`id`),
  KEY `test` (`test_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1403 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for hardest_age_res
-- ----------------------------
DROP TABLE IF EXISTS `hardest_age_res`;
CREATE TABLE `hardest_age_res` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `test_id` int(11) DEFAULT NULL,
  `answer` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `jgfg` (`user_id`),
  KEY `fghfghjeqe` (`test_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2947 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for lesson_gropu_rel
-- ----------------------------
DROP TABLE IF EXISTS `lesson_gropu_rel`;
CREATE TABLE `lesson_gropu_rel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lesson_group_id` int(11) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `sorting` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `egtreg` (`lesson_group_id`),
  CONSTRAINT `egtreg` FOREIGN KEY (`lesson_group_id`) REFERENCES `lessons_group` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=286 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lessons
-- ----------------------------
DROP TABLE IF EXISTS `lessons`;
CREATE TABLE `lessons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `grade` int(11) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lessons_group
-- ----------------------------
DROP TABLE IF EXISTS `lessons_group`;
CREATE TABLE `lessons_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `grade` int(11) NOT NULL,
  `text_pop` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for lessons_test
-- ----------------------------
DROP TABLE IF EXISTS `lessons_test`;
CREATE TABLE `lessons_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test_id` int(11) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  `sorting` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=413 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for migration
-- ----------------------------
DROP TABLE IF EXISTS `migration`;
CREATE TABLE `migration` (
  `version` varchar(180) NOT NULL,
  `apply_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for pre_tests
-- ----------------------------
DROP TABLE IF EXISTS `pre_tests`;
CREATE TABLE `pre_tests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pop_text` text,
  `pop_text_2` text,
  `title` varchar(255) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for pre_tests_res
-- ----------------------------
DROP TABLE IF EXISTS `pre_tests_res`;
CREATE TABLE `pre_tests_res` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `test_id` int(11) DEFAULT NULL,
  `answer` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `time` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `jgfg` (`user_id`),
  KEY `fghfghjeqe` (`test_id`),
  CONSTRAINT `fghfghjeqe` FOREIGN KEY (`test_id`) REFERENCES `tests_question` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `jgfg` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=741 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for region
-- ----------------------------
DROP TABLE IF EXISTS `region`;
CREATE TABLE `region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for schools
-- ----------------------------
DROP TABLE IF EXISTS `schools`;
CREATE TABLE `schools` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region` int(11) DEFAULT NULL,
  `city` int(11) DEFAULT NULL,
  `community` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `number` varchar(255) DEFAULT NULL,
  `level` varchar(255) DEFAULT NULL,
  `addres` varchar(255) DEFAULT NULL,
  `tel` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1398 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for schools_copy
-- ----------------------------
DROP TABLE IF EXISTS `schools_copy`;
CREATE TABLE `schools_copy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `community` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `number` varchar(255) DEFAULT NULL,
  `level` varchar(255) DEFAULT NULL,
  `addres` varchar(255) DEFAULT NULL,
  `tel` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1474 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for tests_question
-- ----------------------------
DROP TABLE IF EXISTS `tests_question`;
CREATE TABLE `tests_question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pre_test_id` int(11) DEFAULT NULL,
  `question` varchar(255) DEFAULT NULL,
  `answer_1` varchar(255) DEFAULT NULL,
  `answer_2` varchar(255) DEFAULT NULL,
  `answer_3` varchar(255) DEFAULT NULL,
  `answer_4` varchar(255) DEFAULT NULL,
  `answer_5` varchar(255) DEFAULT NULL,
  `answer_6` varchar(255) DEFAULT NULL,
  `answer_7` varchar(255) DEFAULT NULL,
  `answer_8` varchar(255) DEFAULT NULL,
  `answer_9` varchar(255) DEFAULT NULL,
  `answer_10` varchar(255) DEFAULT NULL,
  `right_answers` varchar(255) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  `type` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `test` (`pre_test_id`),
  CONSTRAINT `test` FOREIGN KEY (`pre_test_id`) REFERENCES `pre_tests` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2315 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `auth_key` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password_reset_token` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` smallint(6) NOT NULL DEFAULT '10',
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `sex` int(1) NOT NULL,
  `region` int(5) NOT NULL,
  `city` int(5) DEFAULT NULL,
  `community` int(5) DEFAULT NULL,
  `school` int(5) DEFAULT NULL,
  `grade` int(2) DEFAULT NULL,
  `current_grade` int(2) DEFAULT NULL,
  `question_id` int(11) DEFAULT NULL,
  `answer` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `password_reset_token` (`password_reset_token`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for user_pre_tests_all
-- ----------------------------
DROP TABLE IF EXISTS `user_pre_tests_all`;
CREATE TABLE `user_pre_tests_all` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  `lesson_status` int(11) DEFAULT NULL,
  `point` int(11) DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for user_tests_state
-- ----------------------------
DROP TABLE IF EXISTS `user_tests_state`;
CREATE TABLE `user_tests_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  `grade` int(2) DEFAULT NULL,
  `lesson_id` int(11) DEFAULT NULL,
  `point` int(3) DEFAULT NULL,
  `lesson_type` int(1) DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fssdf` (`user_id`),
  CONSTRAINT `fssdf` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=860 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Table structure for video_lesson
-- ----------------------------
DROP TABLE IF EXISTS `video_lesson`;
CREATE TABLE `video_lesson` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `pop_text` text,
  `text_1` text,
  `video_url` varchar(255) DEFAULT NULL,
  `text_2` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8;
