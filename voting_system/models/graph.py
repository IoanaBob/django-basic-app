


class StatGraph():
    def __init__(self, title, values,graph_num):
        self.title = title
        self.values = values
        self.graph_num = graph_num


        self.function_string = "var data_"+str(graph_num)+""" = new google.visualization.DataTable();
        data_"""+str(graph_num)+""".addColumn('string', 'Category');
        data_"""+str(graph_num)+""".addColumn('number', 'Voters');
        data_"""+str(graph_num)+""".addRows(["""
          
        for i,value in enumerate(self.values):
            if(i > 0):
                self.function_string += ","
            self.function_string += str(value)


        self.function_string += """]);

        // Set chart options
        var options_"""+str(graph_num)+""" = {'title':'"""+self.title+"""',
                       'width':'100%',
                       'height':'100%'};

        // Instantiate and draw our chart, passing in some options.
        var chart_"""+str(graph_num)+""" = new google.visualization.PieChart(document.getElementById('chart_div_"""+str(graph_num)+"""'));
        chart_"""+str(graph_num)+""".draw(data_"""+str(graph_num)+""", options_"""+str(graph_num)+""");
"""
