import 'package:flutter/material.dart';
import 'dart:async';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';

import 'package:Snacked/ui/summary/view_model/summary_vm.dart';

 
 class SummaryPage extends StatefulWidget {
  const SummaryPage({super.key, required this.viewModel});
  final SummaryViewModel viewModel;

  @override
  State<SummaryPage> createState() => _SummaryPageState();
 }

class _SummaryPageState extends State<SummaryPage> {
  final TextEditingController _commentsController = TextEditingController();
  Timer? _timer;

  @override
  void initState() {
    super.initState();
    _timer = Timer(widget.viewModel.timerDuration(), () {
      widget.viewModel.showPrompt(context);
    });
  }

  @override
  void dispose() {
    _commentsController.dispose();
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
      return Scaffold (
        appBar: AppBar(
          title: Text('Summary for ${DateFormat('MMMM d, y').format(widget.viewModel.summaryDate)}', style: TextStyle(fontWeight: FontWeight.bold)), 
          backgroundColor: Colors.black, automaticallyImplyLeading:false),
        body: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            children: [
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Text('You spent:', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      const SizedBox(height:10),
                      Text('Approximately 180 min eating,', style: TextStyle(fontSize: 16)),
                      const SizedBox(height:5),
                      Text('60 min were likely to be snacking', style: TextStyle(fontSize: 16)),
                      const SizedBox(height:15),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text('That\'s 30 min less than yesterday', style: TextStyle(fontSize: 16)),
                          const SizedBox(width:5),
                          Icon(Icons.arrow_downward, color: Colors.green, size: 20,)
                        ]
                      ),
                      const SizedBox(height:20),
                      SizedBox(
                        height: 100,
                        child: PieChart(
                          PieChartData(
                            sections: [
                              PieChartSectionData(
                                value: 90,
                                radius: 50,
                                color: Colors.white,
                                title: '',
                              ),
                              PieChartSectionData(
                                value: 10,
                                radius: 50,
                                color: const Color.fromARGB(255, 90, 174, 239),
                                title: '',
                              ),
                            ]
                          )
                        )
                      ),
                      const SizedBox(height:15),
                      Text('10% of total time spent eating', style: TextStyle(fontSize: 16)),
                    ],
                  ),
                ),
              ),
              const SizedBox(height:10),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Text('Based on your goals:', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                      const SizedBox(height:10),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text('You\'re on track, keep it up!', style: TextStyle(fontSize: 16)),
                          const SizedBox(width:10),
                          Icon(Icons.thumb_up, color: Colors.green, size: 20,)
                        ]
                      ),
                    ]
                  ),
                ),
              ),
              const SizedBox(height:10),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Text('Anything that contributed to snacking?', style: TextStyle(fontSize: 16)),
                      const SizedBox(height:15),
                      TextField(
                        controller: _commentsController,
                        decoration: InputDecoration(
                          border: OutlineInputBorder(),
                          hintText: 'Type here: ',
                        ),
                        onChanged: (value) async {
                          if (!await widget.viewModel.updateComments(value)) {
                          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                              content: Text('Unable to save comment.', style: TextStyle(fontSize: 16, color:Colors.red, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
                              duration: const Duration(seconds: 3),
                            )
                          );
                        }
                        }
                      ),
                    ]
                  ),
                ),
              ),
            ],
          )
        )
      );

  }

}





