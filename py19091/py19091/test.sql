

create table t_user (
    id int primary key auto_increment ,
    tel varchar(11) unique not null comment '账号',
    password varchar(32) not null comment '密码',
    status int comment '状态，1 代表未激活、2 代表激活、 3 代表 拉黑',
    reg_time datetime comment '注册时间',
    alipay_user_id varchar(100) comment '支付宝用户id',
    qq_user_id varchar(100) comment 'QQ用户id',
    wx_user_id varchar(100) comment '微信用户id'
);
alter table t_user add alipay_user_id varchar(100);
alter table t_user add qq_user_id varchar(100);
alter table t_user add wx_user_id varchar(100);


create table t_user_info (
    id int primary key auto_increment ,
    email varchar(50) not null ,
    birth date comment '出生日期',
    nickname varchar(100) comment '昵称',
    realname varchar(100) comment '真实姓名',
    sex varchar(1) comment '性别，m代表 男， f 代表女， s 代表 保密',
    photo longblob comment '用户头像',
    user_id int comment '用户ID'
);

create table t_point(
    id int primary key auto_increment,
    point int not null comment '用户积分',
    ch_time datetime comment '积分更改时间',
    source varchar(20) comment '更改积分原因,1用户注册，2上传资料，3评论资源，4下载资源，5发表帖子',
    user_id int comment '用户id，外键'
);

create table t_score_conf(
    id int primary key auto_increment,
    action int comment '动作，1用户注册，2上传资料，3评论资源，4下载资源，5发表帖子',
    score int comment '动作对应的赠送积分数'
);
insert into t_score_conf (action,score) values (1,20);
insert into t_score_conf (action,score) values (2,8);
insert into t_score_conf (action,score) values (3,2);
insert into t_score_conf (action,score) values (5,2);

create table resource_info(
    id int primary key auto_increment,
    re_path varchar(50) comment '资源路径',
    re_name varchar(20) comment '资源名称',
    re_type varchar(20) comment '资源类型',
    key_words varchar(50) comment '资源关键字',
    re_point int comment '资源下载需要的积分',
    re_desc varchar(255) comment '资源描述',
    download_num int comment '资源下载次数',
    re_suffix varchar(20) comment '资源后缀',
    upload_time date comment '资源上传时间',
    user_id int comment '上传用户id',
    re_size float comment '资源大小'
);

-- 资源下载记录表
create table t_resource_download(
    id int primary key auto_increment,
    user_id int comment '下载资源的用户id',
    re_id int comment '下载的资源id',
    download_time datetime comment '下载日期'
);

-- 评论信息表
create table t_resource_comment(
    id int primary key  auto_increment,
    star int comment "星级",
    content text comment "评论内容",
    comment_time datetime comment "评论时间",
    user_id int comment "评论的用户",
    re_id int comment "评论的资源"
);

-- 星级配置表
create table t_star_conf(
    star int comment '星级',
    comment_num int comment '评论条数'
);
insert into t_star_conf (star, comment_num) values (5,30);
insert into t_star_conf (star, comment_num) values (4,15);
insert into t_star_conf (star, comment_num) values (3,10);
insert into t_star_conf (star, comment_num) values (2,6);
insert into t_star_conf (star, comment_num) values (1,0);

-- 收藏表
create table t_collection(
    id int primary key auto_increment,
    re_id int comment '收藏资源id',
    user_id int comment '当前用户id',
    coll_time datetime comment '收藏时间'
);

--用户好友表
create table t_user_friend(
  id int primary key auto_increment,
  user_id int comment '用户id',
  friend_id int comment '好友id',
  create_time datetime comment '用户好友表'
);

--操作记录表
create table t_logger(
  id int primary key auto_increment,
  realname varchar(100) comment '操作的用户',
  func_name varchar(200) comment '操作的视图函数',
  func_param varchar(200) comment '操作的视图函数需要的参数',
  request_url varchar(100) comment '请求的地址',
  exception_code varchar(20) comment '异常编码',
  exception_msg text comment '异常信息',
  create_time datetime comment '日志产生的时间'
);
