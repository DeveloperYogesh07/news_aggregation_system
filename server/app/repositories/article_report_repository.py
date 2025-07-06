from app.models.article_report import ArticleReport


class ArticleReportRepository:
    @staticmethod
    def create(db, article_id, user_id):
        report = ArticleReport(article_id=article_id, user_id=user_id)
        db.add(report)
        db.commit()
        return report

    @staticmethod
    def count_reports(db, article_id):
        return db.query(ArticleReport).filter_by(article_id=article_id).count()
