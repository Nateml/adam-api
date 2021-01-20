from bs4 import BeautifulSoup
import re
import requests


class Session(object):
    """Create a login session to access adam data

    Args:
        username (String): username
        password (String): password 
        type (String): Type of login. Pupil/staff/parent
    """

    def __init__(self, username, password, type):
        """Create a login self.session to access adam data

        Args:
            username (String): username
            password (String): password 
            type (String): Type of login. Pupil/staff/parent
        """

        self.username = username
        self.password = password
        self.type = type

        self.login_url = 'https://adam.oakhill.co.za/proc_login.php'

        self.payload = {
            'username': username,
            'password': password,
            'type': type
        }

        self.session = requests.session()
        response = self.session.post(self.login_url, self.payload)

        self.soup = BeautifulSoup(response.content, 'html.parser')

    def reset(self):
        self.soup = BeautifulSoup(self.session.post(self.login_url, self.payload).content, 'html.parser')

    def get_terms(self):
        """Returns a dictionary with years as keys and lists of terms as values 
        """
        self.reset()
        url = self.soup.find('a', string='Mark book')['href']
        response = self.session.get(url)

        self.soup = BeautifulSoup(response.content, 'html.parser')
        terms = self.soup.find_all('a', string=re.compile('Term'))

        dict = {}
        old_year = 0
        for term in terms:
            parent = term.find_parent('div')
            year = int(parent.find('h3').string)
            if year != old_year:
                old_year = year
                dict[f'{old_year}'] = [term]
            dict[f'{old_year}'].append(term)
        return terms

    def terms_as_list(self):
        """returns html of each term in list format
        """
        years = self.get_terms()
        terms_list = []
        for year in years:
            for term in years:
                terms_list.append('%s, %s' %s (term.string, year))
        
        return terms_list

    def terms(self):
        """returns list of the <a> tag for each term
        """
        years = self.get_terms()
        terms = []
        for year in years:
            for term in year:
                terms.append(term)

        return terms


    def get_marks(self, term_index, subjectName=None):
        """ Returns a dictionary with subjects as keys and lists of tuples (assessment, percent) as values

        Args:
            term_index (int): The index of the term found in the list returned by calling terms() 
            subject (String): subject to retrieve marks from
        """



        marks_dict = {}
        terms = self.get_terms()
        response = self.session.get(
            'https://adam.oakhill.co.za/portal/%s' % (terms[term_index]['href']))

        soup = BeautifulSoup(response.content, 'html.parser')
        
        subject_containers = soup.find_all('div', class_='section col_half')
        marks = []
        for container in subject_containers:
            subject = container.find('th', class_='subjectname').string.split(':')[0]
            assessment_list = container.find_all('td', class_='assessment-percent')
            count = 0
            for i in assessment_list:
                i = i.find_parent('tr')
                try:
                    marks.append((' '.join(i.find('span', class_='assessment-description').string.split()),
                                        i.find('td', class_='assessment-percent').string))
                except AttributeError:
                    pass

                count += 1
            marks_dict[subject] = marks

        if subjectName == None:
            return marks_dict
        else:
            return marks_dict[subjectName.upper()]

if __name__ == "__main__":
    s = Session('n.macdonald', 'Polki1369', 'pupil')
    print(s.get_marks(0, 'English'))



