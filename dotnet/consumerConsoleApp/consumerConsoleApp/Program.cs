using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System;
using System.Diagnostics;
using System.Text;


namespace ConsumeConsoleApp
{
    public static class RabbitConsumer
    {
        static async void RunConsum()
        {
            string host = "amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com:5671/jmnvgeqr";
            var factory = new ConnectionFactory() { Uri = new Uri(host) };
            using var connection = await factory.CreateConnectionAsync();
            using var channel = await connection.CreateChannelAsync();
            using (channel.QueueDeclareAsync(queue: "dotnetRabbit",
                                             durable: false,
                                             exclusive: false,
                                             autoDelete: false,
                                             arguments: null))
            {
                var consumer = new AsyncEventingBasicConsumer(channel);
                consumer.ReceivedAsync += async (model, ea) =>
                    {
                        var body = ea.Body.ToArray();
                        var message = Encoding.UTF8.GetString(body);
                        Debug.WriteLine(" [x] Received {0}", message);
                    };
                string consumerMessage = await channel.BasicConsumeAsync(queue: "dotnetRabbit",
                                         autoAck: true,
                                         consumer: consumer);
                Debug.WriteLine("consumerMessage");
                Debug.WriteLine(consumerMessage);
            }


            static void Main(string[] args)
            {
                RunConsum();
            }

        }
    }
}
