using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System;
using System.Diagnostics;
using System.Text;


namespace consumerConsoleApp
{
    public class Program
    {
        public static async Task Main(string[] args)
        {
            string host = "amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com:5671/jmnvgeqr"; 
            var factory = new ConnectionFactory { HostName = host }; 
            using var connection = await factory.CreateConnectionAsync();
            using var channel = await connection.CreateChannelAsync();
            {
                await channel.QueueDeclareAsync(
                    queue: "dotnetRabbit",
                    durable: false,
                    exclusive: false,
                    autoDelete: false,
                    arguments: null);

                Debug.WriteLine("Waiting for messages. To exit press CTRL+C");

                var consumer = new AsyncEventingBasicConsumer(channel);
                consumer.ReceivedAsync += async (model, ea) =>
                {
                    var body = ea.Body.ToArray();
                    var message = Encoding.UTF8.GetString(body);
                    Debug.WriteLine($" [x] Received: {message}");
                    await Task.CompletedTask;
                };

                await channel.BasicConsumeAsync(
                    queue: "myQueue",
                    autoAck: false,
                    consumer: consumer);
                Console.ReadLine();
            }
        }
    }
}



//static void Main(string[] args)
//Class1 cls = new();
//cls.RunConsumer();
