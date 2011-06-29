import transaction
import datetime

from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy import DateTime
from sqlalchemy import Unicode

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy.schema import UniqueConstraint

from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Subject(Base):
    __tablename__ = 'subjects'

    id   = Column(Integer, primary_key=True)
    # Subject code; 'mast30025'
    code = Column(Unicode(9), unique=True)
    # Full subject name; 'Linear Statistical Models'
    name = Column(String, unique=True)

    # Subject 1  ---> + Section
    sections = relationship("Section")

    def __init__(self, name, code):
        self.name = name
        self.code = code

class Section(Base):
    __tablename__ = 'sections'
    __table_args__ = (
            # Given the subject the setion belongs to, the following
            # fields should be unique: Section Name, URL, Sequence number
            UniqueConstraint('subject_code', 'name'),
            UniqueConstraint('subject_code', 'url'),
            UniqueConstraint('subject_code', 'seq')
        )

    id   = Column(Integer, primary_key=True)
    # Proper name of a section; "Random Variables"
    name = Column(String)
    # Clean URL for a section; "randvars"
    url  = Column(String)
    # Order in which sections appear
    seq  = Column(Integer)

    # Section + <---  1 Subject
    subject_code = Column(String, ForeignKey('subjects.code'))
    # Section 1  ---> + Paragraph
    paragraphs = relationship("Paragraph")

    def __init__(self, name, url, subject_code, seq):
        self.name  = name
        self.url   = url
        self.subject_code = subject_code
        self.seq   = seq

class Paragraph(Base):
    __tablename__ = 'paragraphs'
    __table_args__ = (
            # Given the section the paragraph belongs to,
            # the Sequence field should be unique.
            UniqueConstraint('section_id', 'seq'),
        )

    id   = Column(Integer, primary_key=True)
    # Pre-built HTML to render this paragraph.
    html = Column(String)
    # Integer order in which the paragraphs should appear
    seq  = Column(Integer)

    # Paragraph + <---  1 Section
    section_id = Column(Integer, ForeignKey('sections.id'))
    # Paragraph 1  ---> * Comment
    comments = relationship("Comment")

    def __init__(self, html, seq, section_id):
        self.html = html
        self.seq = seq
        self.section_id = section_id

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    # Name of the author
    name = Column(String)
    # Email contact for the author
    email = Column(String)
    # Date and time comment was submitted
    datetime = Column(DateTime)
    # Text content of the comment
    text = Column(String)

    # Comment * <---  1 Paragraph
    paragraph_id = Column(Integer, ForeignKey('paragraphs.id'))

    def __init__(self, name, email, datetime, text, paragraph_id):
        self.name = name
        self.email = email
        self.datetime = datetime
        self.text = text
        self.paragraph_id = paragraph_id

def initialize_sql(engine):
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    try:
        transaction.begin()
        session = DBSession()

        s1 = Subject('Prob & Stat', 'mast30020')
        session.add(s1)

        sec1 = Section('Sigma algebras',   'sigalg',      'mast30020', 1)
        sec2 = Section('Random variables', 'randvar',     'mast30020', 2)
        sec3 = Section('Expectation',      'expectation', 'mast30020', 3)
        session.add(sec1); session.add(sec2); session.add(sec3)

        para1 = Paragraph('Here is some maths', 1, 1)
        session.add(para1)
        
        comment1 = Comment('AF','a@a.a',datetime.datetime.now(),
                           'That\'s some cool maths.', 1)
        session.add(comment1)

        s2 = Subject('Linear Models', 'mast30025')
        session.add(s2)

        sec1 = Section('Linear Algebra',   'linalg',      'mast30025', 1)
        sec2 = Section('Random variables', 'randvar',     'mast30025', 2)
        sec3 = Section('Expectation',      'expectation', 'mast30025', 3)
        session.add(sec1); session.add(sec2); session.add(sec3)

        transaction.commit()
    except IntegrityError:
        pass
