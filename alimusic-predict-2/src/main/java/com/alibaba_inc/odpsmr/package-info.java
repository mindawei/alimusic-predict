/**
 *@Description:
 *@Author: 闵大为
 *@Since:2016年6月19日
 *@Version:0.1.0
 */

/**
 * 编写参考：http://beader.me/2014/05/05/odps-mapreduce/
 * 
 * 1 输入：  带艺人ID的用户播放行为(已经去除下载、收藏等)
 *  表名：user_actions_combine
 *  字段：artist_id,user_id,song_id,gmt_create,Ds
 * 
 * 2 处理：
 *   2.1 按小时统计
 *   2.2 将超过16的设置为16
 *   2.3 按天输出
 * 
 * 3 输出：按天进行统计
 *  表名： user_actions_count_day
 *  字段：artist_id,Ds,Plays
 *  
 *  
 *  key:artist_id,Ds
 *  value:user_id,song_id,gmt_create
 *  
 */
package com.alibaba_inc.odpsmr;

