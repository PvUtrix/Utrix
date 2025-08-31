// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title FounderVesting
 * @dev Smart contract for managing founder equity vesting
 * 
 * This is a TEMPLATE - Customize for your specific needs
 * Get legal and technical review before deployment
 */

contract FounderVesting {
    struct VestingSchedule {
        address beneficiary;
        uint256 totalShares;
        uint256 startTime;
        uint256 cliffDuration;
        uint256 vestingDuration;
        uint256 releasedShares;
        bool revocable;
        bool revoked;
    }
    
    mapping(address => VestingSchedule) public vestingSchedules;
    address public company;
    uint256 public totalSharesAllocated;
    
    event VestingScheduleCreated(address beneficiary, uint256 shares);
    event SharesReleased(address beneficiary, uint256 shares);
    event VestingRevoked(address beneficiary);
    
    modifier onlyCompany() {
        require(msg.sender == company, "Only company can call");
        _;
    }
    
    constructor() {
        company = msg.sender;
    }
    
    /**
     * @dev Create vesting schedule for a founder
     * Standard: 4 year vesting with 1 year cliff
     */
    function createVestingSchedule(
        address _beneficiary,
        uint256 _totalShares,
        uint256 _startTime,
        uint256 _cliffDuration,
        uint256 _vestingDuration,
        bool _revocable
    ) external onlyCompany {
        require(vestingSchedules[_beneficiary].totalShares == 0, "Schedule exists");
        
        vestingSchedules[_beneficiary] = VestingSchedule({
            beneficiary: _beneficiary,
            totalShares: _totalShares,
            startTime: _startTime,
            cliffDuration: _cliffDuration,
            vestingDuration: _vestingDuration,
            releasedShares: 0,
            revocable: _revocable,
            revoked: false
        });
        
        totalSharesAllocated += _totalShares;
        emit VestingScheduleCreated(_beneficiary, _totalShares);
    }
    
    /**
     * @dev Calculate vested shares for a beneficiary
     */
    function calculateVestedShares(address _beneficiary) public view returns (uint256) {
        VestingSchedule memory schedule = vestingSchedules[_beneficiary];
        
        if (schedule.revoked) {
            return schedule.releasedShares;
        }
        
        if (block.timestamp < schedule.startTime + schedule.cliffDuration) {
            return 0;
        }
        
        if (block.timestamp >= schedule.startTime + schedule.vestingDuration) {
            return schedule.totalShares;
        }
        
        uint256 timeVested = block.timestamp - schedule.startTime;
        uint256 vestedShares = (schedule.totalShares * timeVested) / schedule.vestingDuration;
        
        return vestedShares;
    }
    
    /**
     * @dev Release vested shares to beneficiary
     */
    function releaseShares() external {
        address beneficiary = msg.sender;
        VestingSchedule storage schedule = vestingSchedules[beneficiary];
        
        uint256 vestedShares = calculateVestedShares(beneficiary);
        uint256 releasableShares = vestedShares - schedule.releasedShares;
        
        require(releasableShares > 0, "No shares to release");
        
        schedule.releasedShares += releasableShares;
        
        // Transfer shares logic here
        // This would integrate with your token contract
        
        emit SharesReleased(beneficiary, releasableShares);
    }
    
    /**
     * @dev Revoke vesting (for bad leavers)
     */
    function revokeVesting(address _beneficiary) external onlyCompany {
        VestingSchedule storage schedule = vestingSchedules[_beneficiary];
        
        require(schedule.revocable, "Not revocable");
        require(!schedule.revoked, "Already revoked");
        
        uint256 vestedShares = calculateVestedShares(_beneficiary);
        uint256 unvestedShares = schedule.totalShares - vestedShares;
        
        schedule.revoked = true;
        schedule.totalShares = vestedShares;
        totalSharesAllocated -= unvestedShares;
        
        emit VestingRevoked(_beneficiary);
    }
    
    /**
     * @dev Accelerate vesting (for acquisitions)
     */
    function accelerateVesting(address _beneficiary, uint256 _months) external onlyCompany {
        VestingSchedule storage schedule = vestingSchedules[_beneficiary];
        
        require(!schedule.revoked, "Vesting revoked");
        
        // Reduce vesting duration by specified months
        uint256 acceleration = _months * 30 days;
        if (acceleration >= schedule.vestingDuration) {
            schedule.vestingDuration = 0;
        } else {
            schedule.vestingDuration -= acceleration;
        }
    }
}

/**
 * @title MilestoneRelease
 * @dev Release funds or equity based on milestone achievement
 */
contract MilestoneRelease {
    struct Milestone {
        string description;
        uint256 targetValue;
        uint256 releaseAmount;
        address oracle;
        bool achieved;
        bool released;
    }
    
    Milestone[] public milestones;
    address public company;
    
    modifier onlyCompany() {
        require(msg.sender == company, "Only company");
        _;
    }
    
    constructor() {
        company = msg.sender;
    }
    
    function addMilestone(
        string memory _description,
        uint256 _targetValue,
        uint256 _releaseAmount,
        address _oracle
    ) external onlyCompany {
        milestones.push(Milestone({
            description: _description,
            targetValue: _targetValue,
            releaseAmount: _releaseAmount,
            oracle: _oracle,
            achieved: false,
            released: false
        }));
    }
    
    function checkMilestone(uint256 _milestoneId, uint256 _currentValue) external {
        Milestone storage milestone = milestones[_milestoneId];
        
        require(msg.sender == milestone.oracle, "Only oracle");
        require(!milestone.achieved, "Already achieved");
        
        if (_currentValue >= milestone.targetValue) {
            milestone.achieved = true;
        }
    }
    
    function releaseMilestone(uint256 _milestoneId) external {
        Milestone storage milestone = milestones[_milestoneId];
        
        require(milestone.achieved, "Not achieved");
        require(!milestone.released, "Already released");
        
        milestone.released = true;
        
        // Release logic here
    }
}
