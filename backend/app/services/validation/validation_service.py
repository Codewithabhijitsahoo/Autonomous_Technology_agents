import time
from typing import List, Dict, Any
from app.utils.logger import log

class ValidationCoordinatorService:
    def merge_validation_results(
        self, 
        unique_evidence: List[Dict[str, Any]],
        credibility_scores: Dict[str, Any],
        conflicts: List[Dict[str, Any]],
        confidence_scores: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Merges all independent agent outputs into final validated evidence.
        """
        validated = []
        discarded = []
        
        # Build conflict map
        conflict_map = {}
        for conflict in conflicts:
            for eid in conflict.get("conflicting_evidence_ids", []):
                if eid not in conflict_map:
                    conflict_map[eid] = []
                conflict_map[eid].append(conflict.get("conflict_reason", ""))
        
        for item in unique_evidence:
            eid = item.get("id")
            
            cred_data = credibility_scores.get(eid, {"score": 50, "reason": "No score assigned"})
            conf_data = confidence_scores.get(eid, {"score": 50, "reason": "No score assigned"})
            item_conflicts = conflict_map.get(eid, [])
            
            # Deep copy to avoid mutating original state references unexpectedly
            validated_item = item.copy()
            validated_item["validation_metadata"] = {
                "credibility_score": cred_data["score"],
                "credibility_reason": cred_data["reason"],
                "confidence_score": conf_data["score"],
                "confidence_reason": conf_data["reason"],
                "conflicts": item_conflicts,
                "is_valid": conf_data["score"] >= 30 # Discard very low confidence
            }
            
            if validated_item["validation_metadata"]["is_valid"]:
                validated.append(validated_item)
            else:
                discarded.append(validated_item)
                
        # Generate stats
        total = len(unique_evidence)
        val_count = len(validated)
        avg_conf = sum(i["validation_metadata"]["confidence_score"] for i in validated) / max(1, val_count) if validated else 0
        
        report = {
            "total_processed": total,
            "total_validated": val_count,
            "total_discarded": len(discarded),
            "total_conflicts": len(conflicts),
            "average_confidence": round(avg_conf, 2)
        }
        
        summary = f"Validated {val_count}/{total} items. Avg Confidence: {report['average_confidence']}%. Conflicts found: {report['total_conflicts']}"
        
        return {
            "validated_evidence": validated,
            "discarded_evidence": discarded,
            "validation_report": report,
            "validation_summary": summary
        }
