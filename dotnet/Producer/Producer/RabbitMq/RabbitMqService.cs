using Microsoft.Extensions.Options;
using RabbitMQ.Client;
using System.Diagnostics;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;


namespace Producer.RabbitMq
{
    public class RabbitMqService : IRabbitMqService
    {
        public void SendMessage(object obj)
        {
            var message = JsonSerializer.Serialize(obj);
            SendMessage(message);
        }

        public async void SendMessage(string message)
        {
            string host = "amqps://jmnvgeqr:1FNeqMtZKcTKJSMqPRDVQUj9Oo1iBB-r@chimpanzee.rmq.cloudamqp.com:5671/jmnvgeqr";
            var factory = new ConnectionFactory() { Uri = new Uri(host) };
            using IConnection connection = await factory.CreateConnectionAsync();
            using var channel = await connection.CreateChannelAsync();
            await channel.QueueDeclareAsync(queue: "dotnetRabbit",
                                   durable: false,
                                   exclusive: false,
                                   autoDelete: false,
                                   arguments: null);

            var body = Encoding.UTF8.GetBytes(message);
            await channel.BasicPublishAsync(exchange: String.Empty,
                                   routingKey: "dotnetRabbit",
                                   body: body);
            Debug.WriteLine($" [x] Sent {message}");
        }
    }
}
