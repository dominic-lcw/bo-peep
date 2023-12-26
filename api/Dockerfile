# Use an official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.11

# Copy the current directory contents into the container at /app
COPY . /home
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /home/requirements.txt

ENV PYTHONPATH=/home

# Make port 80 available to the world outside this container
EXPOSE 80

# Run api_cache.py when the container launches
CMD ["lambda_function.handler"]