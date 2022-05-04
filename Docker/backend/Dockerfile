FROM python:3.9.12
COPY entrypoint.sh /entrypoint.sh
COPY CCC_Project2 /CCC_Project2
RUN chmod 755 /entrypoint.sh

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
RUN pip install -r /CCC_Project2/Backend/requirements.txt

# Run at start up
CMD ["python3", "api.py"]
ENTRYPOINT ["/entrypoint.sh"]
