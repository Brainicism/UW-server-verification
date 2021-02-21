import smtplib
import ssl
from email.message import EmailMessage


def _generate_message(email, from_addr, code, name):
    msg = EmailMessage()
    body = (
        f"Your verification code is {code}",
        "\n"
        f"This email was triggered by {name}.",
    )
    msg.set_content("\n".join(body))
    msg['Subject'] = "Email Verification Code from AndrewBot"
    msg['From'] = from_addr
    msg['To'] = str(email)
    return msg


class SMTPMailer(object):
    """A Mailer sends out emails."""
    __slots__ = ["host", "port", "username", "password", "from_addr"]

    def __init__(self, host, port, username, password, from_addr):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_addr = from_addr

    def send(self, address, code, name):
        msg = _generate_message(address, self.from_addr, code, name)
        # TODO: configurable TLS vs STARTTLS
        context = ssl.create_default_context()
        server = smtplib.SMTP(self.host, self.port)
        server.starttls(context=context)
        server.login(self.username, self.password)
        server.send_message(msg)
        server.quit()


class PrintMailer(object):
    """A mailer that just prints things instead of sending for real."""
    __slots__ = []

    def send(self, address, code, name):
        msg = _generate_message(address, "test@example.com", code, name)
        print("Email to send")
        print(msg)
