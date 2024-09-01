create_metrics_db_sql = """
CREATE DATABASE IF NOT EXISTS metrics
"""
create_click_topic_kafka_sql = """
CREATE TABLE IF NOT EXISTS metrics.click_topic (
    user_id String,
    element_id String
) ENGINE = Kafka
SETTINGS kafka_broker_list = '{kafka_host}:{kafka_port}',
         kafka_topic = 'click',
         kafka_group_name = 'click_group',
         kafka_format = 'JSONEachRow'
"""

create_clicks_table_sql = """
CREATE TABLE IF NOT EXISTS metrics.clicks (
    user_id String,
    element_id String
) ENGINE = MergeTree()
ORDER BY user_id
"""

create_clicks_mv_sql = """
CREATE MATERIALIZED VIEW IF NOT EXISTS
metrics.click_mv TO metrics.clicks AS SELECT * FROM metrics.click_topic
"""

create_page_view_topic_kafka_sql = """
CREATE TABLE IF NOT EXISTS metrics.page_view_topic (
    user_id String,
    url String
) ENGINE = Kafka('{kafka_host}:{kafka_port}', 'page_view', 'page_view_group', 'JSONEachRow')
"""

create_page_views_table_sql = """
CREATE TABLE IF NOT EXISTS metrics.page_views (
    user_id String,
    url String
) ENGINE = MergeTree()
ORDER BY user_id
"""

create_page_views_mv_sql = """
CREATE MATERIALIZED VIEW IF NOT EXISTS
metrics.page_view_mv TO metrics.page_views AS SELECT * FROM metrics.page_view_topic
"""

create_video_quality_change_topic_kafka_sql = """
CREATE TABLE IF NOT EXISTS metrics.video_quality_change_topic (
    user_id String,
    video_id String,
    prev_quality String,
    new_quality String
) ENGINE = Kafka('{kafka_host}:{kafka_port}', 'video_quality_change', 'video_quality_change_group', 'JSONEachRow')
"""

create_video_quality_changes_table_sql = """
CREATE TABLE IF NOT EXISTS metrics.video_quality_changes (
    user_id String,
    video_id String,
    prev_quality String,
    new_quality String
) ENGINE = MergeTree()
ORDER BY user_id
"""

create_video_quality_changes_mv_sql = """
CREATE MATERIALIZED VIEW IF NOT EXISTS
metrics.video_quality_change_mv TO metrics.video_quality_changes AS SELECT * FROM metrics.video_quality_change_topic
"""


create_video_view_to_the_end_topic_kafka_sql = """
CREATE TABLE IF NOT EXISTS metrics.video_view_to_the_end_topic (
    user_id String,
    video_id String
) ENGINE = Kafka('{kafka_host}:{kafka_port}', 'video_view_to_the_end', 'video_view_to_the_end_group', 'JSONEachRow')
"""

create_video_views_to_the_end_table_sql = """
CREATE TABLE IF NOT EXISTS metrics.video_views_to_the_end (
    user_id String,
    video_id String
) ENGINE = MergeTree()
ORDER BY user_id
"""

create_video_views_to_the_end_mv_sql = """
CREATE MATERIALIZED VIEW IF NOT EXISTS
metrics.video_view_to_the_end_mv TO metrics.video_views_to_the_end AS SELECT * FROM metrics.video_view_to_the_end_topic
"""


create_search_filters_topic_kafka_sql = """
CREATE TABLE IF NOT EXISTS metrics.search_filters_topic (
    user_id String,
    filter_name String
) ENGINE = Kafka('{kafka_host}:{kafka_port}', 'search_filters', 'search_filters_group', 'JSONEachRow')
"""

create_search_filters_table_sql = """
CREATE TABLE IF NOT EXISTS metrics.search_filters (
    user_id String,
    filter_name String
) ENGINE = MergeTree()
ORDER BY user_id
"""

create_search_filters_mv_sql = """
CREATE MATERIALIZED VIEW IF NOT EXISTS
metrics.search_filters_mv TO metrics.search_filters AS SELECT * FROM metrics.search_filters_topic
"""

clickhouse_init_sql_queries = (
    create_metrics_db_sql,
    create_click_topic_kafka_sql,
    create_clicks_table_sql,
    create_clicks_mv_sql,
    create_page_view_topic_kafka_sql,
    create_page_views_table_sql,
    create_page_views_mv_sql,
    create_video_quality_change_topic_kafka_sql,
    create_video_quality_changes_table_sql,
    create_video_quality_changes_mv_sql,
    create_video_view_to_the_end_topic_kafka_sql,
    create_video_views_to_the_end_table_sql,
    create_video_views_to_the_end_mv_sql,
    create_search_filters_topic_kafka_sql,
    create_search_filters_table_sql,
    create_search_filters_mv_sql,
)
