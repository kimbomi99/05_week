from selenium import webdriver
import unittest

class FuntionalTest(unittest.TestCase):
    class QuestionDetailViewTests(TestCase):
        ...

    def test_has_a_href_link(self):
        """
        Questions with a pub_date in the past are displayed on the
        detail page with a href link to result page.
        """

        question = create_question(question_text="Recent question.", timedelta_from_now=datetime.timedelta(days=-30))
        response = self.client.get(f"/polls/{question.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'href="/polls/{question.id}/results/"')

    class QuestionResultViewTests(TestCase):
        def test_future_question(self):
            """
            The result view of a question with a pub_date in the future
            returns a 404 not found.
            """
            future_question = create_question(question_text='Future question.',
                                              timedelta_from_now=datetime.timedelta(days=5))
            response = self.client.get(f'/polls/{future_question.id}/results/')
            self.assertEqual(response.status_code, 404)

        def test_past_question(self):
            """
            The result view of a question with a pub_date in the past
            displays the question's text.
            """
            past_question = create_question(question_text='Future question.',
                                            timedelta_from_now=datetime.timedelta(days=-5))
            response = self.client.get(f'/polls/{past_question.id}/results/')
            self.assertContains(response, past_question.question_text)

        def test_past_question_with_choices(self):
            """
            The result view of a question with a pub_date in the past
            displays the question's result.
            """
            past_question = create_question(question_text='Future question.',
                                            timedelta_from_now=datetime.timedelta(days=-5))
            choice1 = Choice(question=past_question, choice_text="choice 1")
            choice1.save()
            choice2 = Choice(question=past_question, choice_text="choice 2")
            choice2.save()
            response = self.client.get(f'/polls/{past_question.id}/results/')

            self.assertContains(response, f"Choice: {choice1.choice_text}")
            self.assertContains(response, f"Vote Count: {choice1.votes}")

    def test_go_to_result_page(self):
        self.driver.get("http://localhost:8000/polls/1/")
        a_tag = self.driver.find_element_by_tag_name("a")
        self.assertIn(a_tag.text, "투표 결과 보기")
        a_tag.click()
        self.assertEqual(self.driver.current_url, "http://localhost:8000/polls/1/results/")

        self.assertIn(self.driver.find_element_by_tag_name("h1").text, "What's up?")
        p_tags = self.driver.find_elements_by_tag_name("ul > p")
        self.assertTrue(
            any('Choice:' in p_tag.text for p_tag in p_tags)
        )
        self.assertTrue(
            any('Vote Count:' in p_tag.text for p_tag in p_tags)
        )