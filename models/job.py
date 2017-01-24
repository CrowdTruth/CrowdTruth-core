import datetime
import re, string
import numpy as np

class Job():

	@staticmethod
	def aggregate(units, judgments, config):

		# each output column dict is summed

		agg = {
			'unit' : 'nunique',
			'judgment' : 'count',
			'worker' : 'nunique',
			'duration' : 'mean',
			'metrics.worker.agreement' : 'mean'
		}
		job = judgments.groupby('job').agg(agg)


		# compute job runtime
		runtime = (max(judgments['submitted']) - min(judgments['started']))
		job['runtime'] = float(runtime.days) * 24 + float(runtime.seconds) / 3600
		job['runtime.per_unit'] = job['runtime'] / job['unit']
		job['judgments.per.worker'] = job['judgment'] / job['worker']


		agg = {}
		for col in config.output.values():
			job[col+'.clarity'] = units[col+'.metrics.clarity'].apply(lambda x: np.mean(x))

			#values = units[col].sum()
			#total = sum(values.values())
			#for v in values.keys():
				#job[col+'.'+v] = values[v] / float(total)

 		job = job.reindex_axis(sorted(job.columns), axis=1)
 		



		return job



		'''
		$j->workersCount = count(array_unique($workers));
		$j->workerunitsCount = $count;
		$jpu = intval($j->jobConfiguration->content['workerunitsPerUnit']);
		$uc = intval($j->unitsCount);
		if($uc > 0 and $jpu > 0) $j->completion = $j->workerunitsCount / ($uc * $jpu);
		else $j->completion = 0.00;
		
		if($j->completion>1)
			$j->completion = 1.00; // TODO: HACK
		if($j->completion == 1 || $j->status == 'imported') {
			if($j->status != 'imported') { $j->status = 'finished'; }
			if(!isset($j->finishedAt)) 
				$j->finishedAt = new \MongoDate; 
			
			if(isset($j->startedAt) and isset($j->startedAt->sec))
				$j->runningTimeInSeconds = $j->finishedAt->sec - $j->startedAt->sec;
		}
		$j->realCost = ($count/$j->jobConfiguration->content['unitsPerTask'])*$j->jobConfiguration->content['reward'];
		// METRICS
		//if(($j->completion > .25) and ($j->latestMetrics < .25)){
		// If a page is done and there's a proper annotationVector...
		try {

				
				$command = Config::get('config.python_path') . " " . Config::get('config.metrics_path') . " {$j->_id } $templateid";
				//$command = "C:\Users\IBM_ADMIN\AppData\Local\Enthought\Canopy\User\python.exe $apppath/lib/generateMetrics.py {$j->_id } $templateid";
				\Log::debug("Command: $command");
				exec($command, $output, $return_var);
				\Log::debug("Metrics done.");
				
				//dd($output);
				$response = json_decode($output[0], true);
				
				if(!$response or !isset($response['metrics']))
					throw new Exception("Incorrect response from generateMetrics.py.");
					
				// update list of spammers
				foreach($response['metrics']['spammers']['list'] as $spammer) {
					$response['metrics']['workers']['withoutFilter'][$spammer]['spam'] = 1;
				}           
					
				$j->metrics = $response['metrics'];
				$r = $j->results;
				$r['withoutSpam'] = $response['results']['withoutSpam'];
				$j->results = $r;
				$j->spam = $response['metrics']['filteredWorkerunits']['count'] / $j->workerunitsCount * 100;
				
				//\Log::debug(end($output));
				//$j->latestMetrics = .25;
			
				$this->createMetricActivity($j->_id);
				$j->save();
					
				// update workerunits
				foreach ($workerunits as $workerunit) {
					//set_time_limit(60);
					\Queue::push('Queues\UpdateWorkerunits', array('workerunit' => serialize($workerunit)));
				}
				// update worker cache
				foreach ($response['metrics']['workers']['withoutFilter'] as $workerId => $workerData) {
					//set_time_limit(60);
					$agent = CrowdAgent::where("_id", $workerId)->first();
					\Queue::push('Queues\UpdateCrowdAgent', array('crowdagent' => serialize($agent)));
				}
		
				// create output units
				/*
				foreach ($response['results']['withoutSpam'] as $unitId => $content) {
					set_time_limit(60);
					$unit = Unit::where("_id", $unitId)->first();
					
					// create new settings copied from the job
					$settings = [];
					$settings['project'] = $j['project'];
					$settings['format'] = $j['format'];
					$settings['domain'] = $j['domain'];
					$settings['documentType'] = $j['resultType'];
					
					// merge existing content with new generated content
					$newcontent = array_merge($content, $unit['content']);
					$childUnit = Unit::store($settings, $unitId, $newcontent);
				}
				*/
				
				// update input units
				$units = array_keys($response['metrics']['units']['withSpam']);
				\Queue::push('Queues\UpdateUnits', $units);
			
			
			}
		} catch (Exception $e) {
			\Log::debug("Error in running metrics: {$e->getMessage()}");
			echo $e->getMessage();
		}
		//
		//dd($j);
		$j->save();
		\Log::debug("Updated Job {$j->_id}.");
		$job->delete(); // This is the Queue job and not our Job!
	}
	'''
